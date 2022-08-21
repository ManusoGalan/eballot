from datetime import datetime, timezone
from rest_framework import serializers

from .models import BallotBox, Candidate

class BallotBoxCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BallotBox
        fields = ['id', 'name', 'start_datetime', 'end_datetime']
    
    # Here, instead of calling validate(), we call validate_<field_name>(), which valdiates that one field
    def validate_start_datetime(self, value):
        if value < datetime.now(timezone.utc):
            raise serializers.ValidationError('Start datetime must be before creation datetime')
        
        return value
    
    def validate_end_datetime(self, value):
        datetime_without_timezone = datetime.fromisoformat(self.initial_data['start_datetime'].replace("Z", "+00:00"))
        if value < datetime.combine(datetime_without_timezone.date(), datetime_without_timezone.time(), tzinfo=timezone.utc):
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
    
        
class BallotBoxExternalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BallotBox
        fields = ['contractAddress']
        
class CandidateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['name', 'img_path', 'description', 'website', 'motto']
        
    def validate(self, attrs):
        attrs['ballot_parent'] = BallotBox.objects.get(id=self.context['ballot_parent_id'])
        attrs['pk_inside_ballot'] = int(self.context["last_candidate_id"]) + 1
        
        return super().validate(attrs)
    
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
        if(candidate.ballot_parent.end_datetime < datetime.now(timezone.utc)):
            return 100

        return None
    