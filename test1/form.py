from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Userss
"""
class SignUpForm(UserCreationForm):
    last_name = forms.CharField(
    max_length=100,
    required = True,
    help_text='Enter Last Name',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    )
    username = forms.CharField(
    max_length=200,
    required = True,
    help_text='Enter Username',
    widget=forms.TextInput(attrs={'class': 'form-control form-control-lg mb-2', 'placeholder': 'Username'}),
    )
    
    
    password1 = forms.CharField(
    help_text='Enter Password',
    required = True,
    widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg mb-2', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
    required = True,
    help_text='Enter Password Again',
    widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg mb-2', 'placeholder': 'Password Again'}),
    )
    check = forms.BooleanField(required = True)
        
    class Meta:
        model = User
        fields = [
        'username', 'password1', 'password2', 'check',
    ]
    

    class Meta:
        model = Userss
        fields = ('userid', 'userpw','userpw2')
        widgets = {
            'userid': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-lg'
                }
            ),
            'userpw': forms.PasswordInput(
                attrs={
                    'class': 'form-control form-control-lg'
                }
            ),
            'userpw2': forms.PasswordInput(
                attrs={
                    'class': 'form-control form-control-lg'
            }
            )
        }
"""

class SignUpForm(forms.ModelForm):
    class Meta:
        model = Userss
    
        fields = ['userid', 'userpw','userpw2']
        widgets = {
            'userid': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-lg'
                }
            ),
            'userpw': forms.PasswordInput(
                attrs={
                    'class': 'form-control form-control-lg'
                }
            ),
            'userpw2': forms.PasswordInput(
                attrs={
                    'class': 'form-control form-control-lg'
                }
            )
        }
        