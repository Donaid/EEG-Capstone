from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import Userss

# class SignUpForm(UserCreationForm):
#     class Meta:
#         model = Userss
#         fields = ('userid', 'userpw')
        
"""
class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = Userss
        fields = ('userid', 'userpw', 'password1', 'password2', )
"""