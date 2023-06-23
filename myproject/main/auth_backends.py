from django.contrib.auth.backends import ModelBackend
from .models import Registration

class RegistrationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        registrations = Registration.objects.filter(username=username)

        for user in registrations:
            if user.password == password:
                return user
        
        return None

    def get_user(self, user_id):
        try:
            return Registration.objects.filter(pk=user_id).first()
        except Registration.DoesNotExist:
            return None