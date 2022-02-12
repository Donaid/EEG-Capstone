from django.contrib.auth.models import AbstractUser, UserManager as AbstractUserManager
from django.db import models



#from django.conf import settings
#settings.configure(DEBUG=True)

class UserManager(models.Model):
  pass

#Users database table
class Userss(models.Model):
    userid = models.CharField(max_length=20)
    userpw = models.CharField(max_length=50)
    userpw2 = models.CharField(max_length=50)
    objects = UserManager()
    USERNAME_FIELD = 'userid55'
    REQUIRED_FIELDS = []

    
#State Database Table
class State(models.Model):
   user = models.ForeignKey(Userss, on_delete=models.CASCADE)
   attrention = models.FloatField(max_length=20)
   session_no = models.IntegerField()
   timestemp = models.DateTimeField()
   date = models.DateField()
   learning_method = models.CharField(max_length=200)

#Feature Database Table
class feature(models.Model):
    user_id = models.IntegerField()
    attention = models.FloatField(max_length=20)
    
#Machine status
class Machine_status(models.Model):
    stat = models.CharField(max_length=20)
    
class userData(models.Model):
    userName = models.CharField(max_length=20)
    idealStudyTime = models.CharField(max_length=20)
    audioVideoHighAttention = models.CharField(max_length=20)
    readWriteHighAttention = models.CharField(max_length=20)
    sessionsCompletedAV = models.CharField(max_length=20)
    sessionsCompletedRW = models.CharField(max_length=20)
    highToTotalAV = models.CharField(max_length=20)
    highToTotalRW = models.CharField(max_length=20)
    graphHighAttention = models.CharField(max_length=20)
    graphLowAttention = models.CharField(max_length=20)
    