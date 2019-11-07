from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

CONFIRMATIONS = (
    ('Y', 'Yes'),
    ('N', 'No'),
    ('M', 'Maybe')
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    birthday = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True)


class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    address = models.TextField(max_length=250)
    date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    occasion = models.TextField(max_length=150)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'event_id': self.id})

      
class Attendant(models.Model):
    date = models.DateField('confirmation date')
    confirmation = models.CharField(
        max_length=1,
        choices=CONFIRMATIONS,
        default=CONFIRMATIONS[0][0]
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def get_children(comment_id):
        return Comment.objects.filter(parent=comment_id)
