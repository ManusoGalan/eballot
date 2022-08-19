from datetime import datetime
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
        
    def validate(self, attrs):
        attrs['ballot_parent'] = BallotBox.objects.get(id=self.context['ballot_parent'])
        return super().validate(attrs)
class SimpleCandidateSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'result']
        
    def get_result(self, candidate):
        return 100