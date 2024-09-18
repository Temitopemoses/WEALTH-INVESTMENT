from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            # Try to fetch the user by email
            user = User.objects.get(username=username)
            print(user)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            return None
        except User.DoesNotExist:
            print(f"User does not exist: {username}")

        # if user.check_password(password) and self.user_can_authenticate(user):
        #     return user
        # return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
