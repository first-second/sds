from datetime import date
from django import forms
from django.forms import ModelForm
from .models import Registration
#form page setup visible in register webpage

class RegistrationForm(ModelForm):
    class Meta:
        model = Registration
        fields =('name','address','phone','email_address',)
        labels = {
            'name':'',
            'address':'select the city',
            'phone':'',
            'email_address':'',
        }
        addresslist = (
            ('ghaziabad','ghaziabad'),
            ('gurgaon','gurgaon'),
            ('karnal','karnal'),
            ('mumbai','mumbai'),
            ('punjab','punjab'),
            ('shimla','shimla'),
        )

        widgets = { 
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'ENTER YOUR NAME','style': 'max-width: 500px'}),
            'address': forms.Select(choices=addresslist),
            'phone': forms.TextInput(attrs={'class':'form-control','placeholder':'ENTER YOUR PHONE NUMBER','style': 'max-width: 500px'}),
            'email_address': forms.EmailInput(attrs={'class':'form-control','placeholder':'ENTER YOUR EMAIL ID','style': 'max-width: 500px'}),
        }
    
