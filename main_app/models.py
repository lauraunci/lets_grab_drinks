from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    location = models.CharField(max_length=50)
    birthday = models.DateField(auto_now=False, auto_now_add=False)
