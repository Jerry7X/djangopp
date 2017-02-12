from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class TotalCount(models.Model):
    id = models
    total = models.FloatField()
    left = models.FloatField()

class Deposit(models.Model):
    name = models.CharField(max_length=64)
    amount = models.FloatField(default=0)
    time = models.DateField(default=datetime.date.today())

class MemberCount(models.Model):
    name = models.CharField(max_length=64)
    t_amount = models.FloatField(default=0)
    l_amount = models.FloatField(default=0)

class PlayOne(models.Model):
    time = models.DateField()
    players = models.TextField()
    place = models.CharField(max_length=64)
    duration = models.IntegerField()
    fee = models.FloatField()
    ballused = models.IntegerField()
    balltype = models.CharField(max_length=64)
    aaprice = models.FloatField()

class Ball(models.Model):
    name = models.CharField(max_length=64)
    count = models.IntegerField()
    price = models.FloatField()
    l_count = models.IntegerField(default=0)




