from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

# pay/consume history
class Deposit(models.Model):
    name = models.CharField(max_length=64)
    amount = models.FloatField(default=0)
    time = models.DateField()

# amount can be as -10
class Member(models.Model):
    name = models.CharField(max_length=64)
    amount = models.FloatField(default=0)

class Play(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.DateField()
    play_time = models.CharField(max_length=64)
# place and duration is used for notify.
    place = models.CharField(max_length=64)
    duration = models.CharField(max_length=64)
    fee = models.FloatField()
    aaprice = models.FloatField()
# start:1, running:2; end:3; cancel: 4
    state = models.IntegerField()
    fee_comment = models.CharField(max_length=64)

class Apply(models.Model):
    name = models.CharField(max_length=64)
    pid = models.IntegerField()

class Ball(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()
# where to buy it? or something else
    desc = models.CharField(max_length=64)



