from dataclasses import fields
from pyexpat import model
from rest_framework import serializers

from .models import BallotBox, Candidate

class BallotBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = BallotBox
        fields = ['id', 'name', 'initTimestamp', 'endTimestamp', 'contractAddress']
        
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'imgPath', 'description', 'website', 'moto']