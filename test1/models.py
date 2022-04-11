from email.policy import default
from django.contrib.auth.models import AbstractUser, UserManager as AbstractUserManager, User
from django.db import models
from django.forms import DateTimeField

READWRITE = 'r'
AURALVISUAL = 'w'

learningMethodChoices = [
    (READWRITE, "readwrite"),
    (AURALVISUAL, "auralvisual")
]

class State(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    attention = models.FloatField()
    session = models.IntegerField()
    learningMethod = models.CharField(max_length=1, choices=learningMethodChoices)

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latestSession = models.IntegerField()
    consecutiveHighR = models.IntegerField(default=0)
    consecutiveHighW = models.IntegerField(default=0)

    