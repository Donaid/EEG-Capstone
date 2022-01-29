from django.db import models


#from django.conf import settings
#settings.configure(DEBUG=True)


#Users database table
class Users(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=200)
    
#State Database Table
class State(models.Model):
   user = models.ForeignKey(Users, on_delete=models.CASCADE)
   attrention = models.FloatField(max_length=20)
   session_no = models.IntegerField()
   timestemp = models.DateTimeField()
   date = models.DateField()
   learning_method = models.CharField(max_length=200)

#Feature Database Table
class feature(models.Model):
    user_id = models.IntegerField()
    attention = models.FloatField(max_length=20)
    
