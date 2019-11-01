# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import user_logged_in

User = get_user_model()


class DrupalAuthBackend:
    def authenticate(self, request, username=None, password=None):
        user_logged_in.disconnect(update_last_login)
        try:
            user = User.objects.get(username=username, is_active=True)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
