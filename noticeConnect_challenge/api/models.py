from django.db import models
from .constants import *

# Create your models here.

class Notice(models.Model):
    notice_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    alt_first_name = models.CharField(max_length=100, blank=True)
    alt_last_name = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100)
    date_of_birth = models.DateField()

class Record(models.Model):
    record_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    province = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField()

class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    notice_id = models.IntegerField()
    record_id = models.IntegerField()
    match_type = models.CharField(choices=MATCH_CHOICES, max_length=100)