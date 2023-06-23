from django.contrib.auth.backends import ModelBackend
from .models import Registration

class RegistrationBackend(ModelBackend):
    def authenticate(self, request, email_address=None, password=None, **kwargs):
        try:
            user = Registration.objects.get(email_address=email_address)
            if user.password == password:
                return user
        except Registration.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Registration.objects.get(pk=user_id)
        except Registration.DoesNotExist:
            return None
