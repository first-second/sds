from django.contrib.auth.backends import ModelBackend
from .models import Registration
from django.contrib.auth.hashers import check_password


class RegistrationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Registration.objects.get(username=username)
            if check_password(password, user.password):
                return user
        except Registration.DoesNotExist:
            pass
        
        return None

    def get_user(self, user_id):
        try:
            return Registration.objects.get(pk=user_id)
        except Registration.DoesNotExist:
            return None
