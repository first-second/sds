from __future__ import unicode_literals
from sqlite3 import Timestamp # read all languages
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Main(models.Model):
    name = models.TextField()
    about = models.TextField()

    def __str__(self):
        return self.name

class Registration(models.Model):
    name = models.CharField(("Full Name"), max_length=50)
    address = models.CharField(("Address"), max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$', message="Phone number must be entered in the format: '+999999999'. 10 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=10, blank=True,unique=True)
    #phone = models.IntegerField(("Phone"),unique=True)
    email_address = models.EmailField(("Email Address"), max_length=254)
    date = models.DateField(auto_now_add=True,auto_now=False,blank=True)

    def __str__(self):
        return self.name 