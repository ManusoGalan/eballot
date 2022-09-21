from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

from .contract import get_abi, get_bytecode

from datetime import datetime
from django.utils import timezone
from rest_framework import serializers

from .models import BallotBox, Candidate

import os
from dotenv import load_dotenv, find_dotenv

class BallotBoxCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BallotBox
        fields = ['id', 'name', 'start_datetime', 'end_datetime']
    
    # Here, instead of calling validate(), we call validate_<field_name>(), which valdiates that one field
    def validate_start_datetime(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('Start datetime must be before creation datetime')
        
        return value
    
    def validate_end_datetime(self, value):
        start_datetime_without_timezone = datetime.fromisoformat(self.initial_data['start_datetime'])
        if value < datetime.combine(start_datetime_without_timezone.date(), start_datetime_without_timezone.time(), tzinfo=timezone.get_current_timezone()):
            raise serializers.ValidationError('End datetime must be after start datetime')
        
        return value
    
class BallotBoxListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BallotBox
        fields = ['id', 'name', 'start_datetime', 'end_datetime']
    
class BallotBoxRetrieveSerializer(serializers.ModelSerializer):
    candidates = serializers.SerializerMethodField()
    class Meta:
        model = BallotBox
        fields = ['id', 'name', 'start_datetime', 'end_datetime', 'candidates']
    
    # As candidates aren't part of the model, we have to tell Django how to retrieve them   
    def get_candidates(self, instance):
        candidateQuery = Candidate.objects.filter(ballot_parent = instance)
        return CandidateRetrieveForBallotSerializer(candidateQuery, many = True).data
    
        
class BallotBoxContractAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BallotBox
        fields = ['contract_address']
        
class CandidateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['name', 'img_path', 'description', 'website', 'motto']
        
    def validate(self, attrs):
        attrs['ballot_parent'] = BallotBox.objects.get(id=self.context['ballot_parent_id'])
        attrs['pk_inside_ballot'] = int(self.context['last_candidate_id']) + 1
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        self.deploy_contract(validated_data)
        return super().create(validated_data)
    
    def deploy_contract(self, validated_data):
        load_dotenv(find_dotenv())
        
        w3 = Web3(HTTPProvider('https://polygon-mumbai.infura.io/v3/' + os.environ['INFURA_API_KEY']))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        admin_account = w3.eth.account.privateKeyToAccount(os.environ['ACCOUNT_KEY'])
        contract = w3.eth.contract(abi=get_abi(), bytecode=get_bytecode())
        
        candidateNames = []
        candidatesPositionInsideBallot = []
        for candidate in Candidate.objects.all().filter(ballot_parent_id=validated_data['ballot_parent'].id):
            candidateNames.append(Web3.toHex(text=candidate.name))
            candidatesPositionInsideBallot.append(candidate.pk_inside_ballot)
        candidateNames.append(Web3.toHex(text=validated_data['name']))
        candidatesPositionInsideBallot.append(validated_data['pk_inside_ballot'])
        
        txn = \
            contract.constructor(
                candidateNames,
                candidatesPositionInsideBallot,
                int(datetime.timestamp(validated_data['ballot_parent'].end_datetime)),
                int(datetime.timestamp(validated_data['ballot_parent'].start_datetime))
            ).buildTransaction(
                {
                    'from': admin_account.address,
                    'nonce': w3.eth.getTransactionCount(admin_account.address),
                }
            ); 
        signed_txn = admin_account.signTransaction(txn)
            
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
        
        validated_data['ballot_parent'].contract_address = txn_receipt['contractAddress']
        validated_data['ballot_parent'].save()
        
class CandidateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['pk_inside_ballot', 'name', 'img_path', 'description', 'website', 'motto']
    
class CandidateRetrieveForBallotSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()
    class Meta:
        model = Candidate
        fields = ['pk_inside_ballot', 'name', 'result']
        
    def get_result(self, candidate):
        if(candidate.ballot_parent.end_datetime < timezone.now()):
            w3 = Web3(HTTPProvider('https://polygon-mumbai.infura.io/v3/' + os.environ['INFURA_API_KEY']))
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            
            contract = w3.eth.contract(abi=get_abi(), address=candidate.ballot_parent.contract_address)
            
            result = contract.functions.getProposalVoteCount(candidate.pk_inside_ballot, int(datetime.timestamp(timezone.now()))).call()
            
            return result

        return None
    