# user/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(CustomUser.USERNAME_FIELD)
        
        try:
            # Try to fetch the user by email
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            try:
                # Try to fetch the user by mobile number
                user = CustomUser.objects.get(mobile_number=username)
            except CustomUser.DoesNotExist:
                try:
                    # Try to fetch the user by username
                    user = CustomUser.objects.get(username=username)
                except CustomUser.DoesNotExist:
                    return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
