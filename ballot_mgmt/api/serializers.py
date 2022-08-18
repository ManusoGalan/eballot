from dataclasses import fields
from pyexpat import model
from rest_framework import serializers

from .models import BallotBox, Candidate

class BallotBoxSerializer(serializers.ModelSerializer):
    candidates = serializers.SerializerMethodField()
    class Meta:
        model = BallotBox
        fields = ['id', 'name', 'initTimestamp', 'endTimestamp', 'candidates']
        
    def get_candidates(self, ballot):
        candidateQuery = Candidate.objects.filter(ballotParent = ballot)
        return SimpleCandidateSerializer(candidateQuery, many = True).data
        
class BallotBoxContractAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BallotBox
        fields = ['contractAddress']
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'imgPath', 'description', 'website', 'motto', 'ballotParent']
        
class SimpleCandidateSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'result']
        
    def get_result(self, candidate):
        return 100