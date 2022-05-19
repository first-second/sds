from datetime import date
from django import forms
from django.forms import ModelForm
from .models import Registration

class RegistrationForm(ModelForm):
    class Meta:
        model = Registration
        fields =('name','address','phone','email_address',)
        labels = {
            'name':'',
            'address':'',
            'phone':'',
            'email_address':'',
        }
        widgets = { 
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'ENTER YOUR NAME','style': 'max-width: 500px'}),
            'address': forms.TextInput(attrs={'class':'form-control','placeholder':'ENTER YOUR ADDRESS','style': 'max-width: 500px'}),
            'phone': forms.TextInput(attrs={'class':'form-control','placeholder':'ENTER YOUR PHONE NUMBER','style': 'max-width: 500px'}),
            'email_address': forms.EmailInput(attrs={'class':'form-control','placeholder':'ENTER YOUR EMAIL ID','style': 'max-width: 500px'}),
        }
    
