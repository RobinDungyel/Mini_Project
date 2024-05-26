from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Position(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.title

    

class Candidate(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/')
    manifesto = models.TextField(default='Manifesto text to be updated')
    total_vote = models.IntegerField(default=0, editable=False)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.name, self.position.title)

class ControlVote(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {} - {}".format(self.user, self.position, self.status)

from datetime import timedelta

class Time(models.Model):
    voting_start = models.DateTimeField()
    voting_end = models.DateTimeField()

    def __str__(self):
        return "{} - {}".format(self.voting_start, self.voting_end)
    
    def is_voting_open(self):
        now = timezone.now()
        if self.voting_start is None or self.voting_end is None:
            return False
        # Adjust the current time by 5.5 hours ahead
        now += timedelta(hours=5, minutes=30)
        return self.voting_start <= now <= self.voting_end
    
