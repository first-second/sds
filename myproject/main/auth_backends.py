from django.contrib.auth.backends import ModelBackend
from .models import Registration

class RegistrationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            print(f"Number of Records: {Registration.objects.filter(username=username).count()}")
            user = Registration.objects.get(phone=username)
            if user.password == password:
                return user
        except Registration.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Registration.objects.get(pk=user_id)
        except Registration.DoesNotExist:
            return None
