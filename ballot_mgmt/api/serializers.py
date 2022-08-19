from dataclasses import fields
from pyexpat import model
from rest_framework import serializers

from .models import BallotBox, Candidate

class BallotBoxSerializer(serializers.ModelSerializer):
    candidates = serializers.SerializerMethodField()
    class Meta:
        model = BallotBox
        fields = ['id', 'name', 'start_datetime', 'end_datetime', 'candidates']
        
    def get_candidates(self, ballot):
        candidateQuery = Candidate.objects.filter(ballot_parent = ballot)
        return SimpleCandidateSerializer(candidateQuery, many = True).data
        
class BallotBoxContractAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BallotBox
        fields = ['contractAddress']
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'img_path', 'description', 'website', 'motto']
class SimpleCandidateSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'result']
        
    def get_result(self, candidate):
        return 100