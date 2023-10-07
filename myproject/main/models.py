from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class Main(models.Model):
    username = models.TextField()
    about = models.TextField()

    def __str__(self):
        return self.username

class RegistrationManager(BaseUserManager):
    """
    custom methods for creating and managing users
    """
    def create_user(self, username, email_address, password=None, address=None, phone=None,photo=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set.")

        user = self.model(username=username, email_address=email_address, address=address, phone=phone, **extra_fields)
        user.set_password(password)
        if photo:
            user.photo = photo
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email_address, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email_address, password, **extra_fields)

class Registration(AbstractBaseUser):
    """"
    Custom user model
    """
    username = models.CharField(("Full Name"), max_length=50)
    address = models.CharField(("Address"), max_length=20)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10}$',
        message="Phone number must be entered in the format: '+999999999'. 10 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=10, blank=True, unique=True)
    email_address = models.EmailField(("Email Address"), max_length=254)
    date = models.DateField(default=timezone.now)
    password = models.CharField(("Password"), max_length=50)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    #username field will be used as unique identifier
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    #RegistrationManager will be used for managing user objects
    objects = RegistrationManager()

    def __str__(self):
        return self.username
