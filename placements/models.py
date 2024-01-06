from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxValueValidator
from datetime import datetime

# Create your models here.
class NewUser(AbstractUser):
    user_type = models.CharField(max_length=100, default='job seeker')
    phone_no = models.CharField(max_length=100, default='9999999999')
    country = models.CharField(max_length=300, default='India')
    state = models.CharField(max_length=300, default='Karnataka')
    address = models.CharField(max_length=100, default='abc')
    city = models.CharField(max_length=100, default='hubli')
    about = models.CharField(max_length=1000, default='about')
    profile = models.ImageField(upload_to='uploaded_images/',default="profile")
    status = models.BooleanField(default=0)
