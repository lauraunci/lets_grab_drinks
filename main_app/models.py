from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    address = models.TextField(max_length=250)
    date_time = models.DateTimeField('event date')
    occasion = models.TextField(max_length=150)
    creator = models.ForeignKey(User, on_delete=models.CASCADE) 