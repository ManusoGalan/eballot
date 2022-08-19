from enum import auto
from unicodedata import name
from django.db import models

# Create your models here.

class BallotBox(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    contract_address = models.CharField(max_length=44, unique=True, blank=True, null=True)
    
class Candidate(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32)
    img_path = models.ImageField()
    description = models.CharField(max_length=500)
    website = models.URLField(blank=True, null=True)
    motto = models.CharField(max_length=100, blank=True, null=True)
    ballot_parent = models.ForeignKey(to=BallotBox, on_delete=models.CASCADE)
    
    def get_result(self, obj):
        return 100