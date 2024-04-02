from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Query using Q object to match either email or phone_no
            user = UserModel.objects.get(Q(email=username) | Q(phone_no=username))
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None