from enum import auto
from unicodedata import name
from django.db import models

# Create your models here.

class BallotBox(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    initTimestamp = models.DateTimeField(blank=False, null=False)
    endTimestamp = models.DateTimeField(blank=False, null=False)
    contractAddress = models.CharField(max_length=44, unique=True)
    
class Candidate(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=32, blank=False, null=False)
    imgPath = models.ImageField()
    description = models.CharField(max_length=500, blank=False, null=False)
    website = models.URLField()
    motto = models.CharField(max_length=100)
    ballotParent = models.ForeignKey(to=BallotBox, on_delete=models.CASCADE, blank=False, null=False)