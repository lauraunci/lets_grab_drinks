from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

CONFIRMATIONS = (
    ('Y', 'Yes'),
    ('N', 'No'),
    ('M', 'Maybe')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    location = models.CharField(max_length=50)
    birthday = models.DateField(auto_now=False, auto_now_add=False)

class Attendant(models.Model):
    confirmations = models.CharField(
        max_length=1,
        choices=CONFIRMATIONS,
        default=CONFIRMATIONS[0][0]
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    address = models.TextField(max_length=250)
    date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    occasion = models.TextField(max_length=150)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    attendants = models.ManyToManyField(Attendant) 

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'event_id': self.id})


    