from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.
class TotalCount(models.Model):
    total = models.FloatField()
    left = models.FloatField()

class Deposit(models.Model):
    name = models.CharField(max_length=64)
    amount = models.FloatField(default=0)
    time = models.DateTimeField(default=timezone.now)
