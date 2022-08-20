from datetime import datetime, timezone
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
    
    def validate_start_datetime(self, value):
        if value < datetime.now(timezone.utc):
            raise serializers.ValidationError('Start datetime must be before creation datetime')
        
        return value
    
    def validate_end_datetime(self, value):
        datetime_without_timezone = datetime.fromisoformat(self.initial_data['start_datetime'].replace("Z", "+00:00"))
        if value < datetime.combine(datetime_without_timezone.date(), datetime_without_timezone.time(), tzinfo=timezone.utc):
            raise serializers.ValidationError('End datetime must be after start datetime')
        
        return value
        
class BallotBoxContractAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BallotBox
        fields = ['contractAddress']
        
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'img_path', 'description', 'website', 'motto']
        
    def validate(self, attrs):
        attrs['ballot_parent'] = BallotBox.objects.get(id=self.context['ballot_parent_id'])
        return super().validate(attrs)
    
class SimpleCandidateSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'result']
        
    def get_result(self, candidate):
        return 100
    