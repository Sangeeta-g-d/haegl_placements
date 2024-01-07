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


class CompanyDetails(models.Model):
    company_id=models.ForeignKey('NewUser', on_delete=models.CASCADE)
    tag_line = models.CharField(max_length=700, default='tagline')
    company_type = models.CharField(max_length=100, default='startup')
    company_service_sector = models.CharField(max_length=1000, default='IT Services')
    why_us = models.CharField(max_length=2000, default='abcd')
    founded_year = models.PositiveIntegerField(
        validators=[MaxValueValidator(datetime.now().year)]  # Maximum year as current year
    )
    head_branch = models.CharField(max_length=500,default='hubli')
    milestone = models.CharField(max_length=4000,default='none')
    linkedin_url = models.URLField(max_length=500,default='https://example.com')
    instagram_url = models.URLField(max_length=500,default='https://example.com')
    facebook = models.URLField(max_length=500,default='https://example.com')
    webiste = models.URLField(max_length=500,default='https://example.com')
    Key_highlights = models.CharField(max_length=2000, default='highlights')
    cover_image = models.ImageField(upload_to='company_images/',default="cover_image")
    other_image1 = models.ImageField(upload_to='company_images/',default='img1')
    other_image2 = models.ImageField(upload_to='company_images/',default='img2')
    

class JobDetails(models.Model):
    company_id = models.ForeignKey('NewUser', on_delete=models.CASCADE)
    designation = models.CharField(max_length=300,default='data analyst')
    job_description = models.CharField(max_length=1000,default='abc')
    department = models.CharField(max_length=300,default='sales')
    location = models.CharField(max_length=300,default='hubli')
    work_mode = models.CharField(max_length=100,default='work from office')
    no_of_vacancy = models.CharField(max_length=100,default='2')
    mandatory_skills = models.CharField(max_length=500,default='HTML')
    optional_skills = models.CharField(max_length=500,default='C')
    experience = models.CharField(max_length=200,default='fresher')
    salary = models.CharField(max_length=400,default='3LPA')
    qualification = models.CharField(max_length=300,default='BCA')
    created_on = models.DateField(auto_now_add = True)
    status = models.CharField(max_length=10, default='open')
    job_type = models.CharField(max_length=100, default='Full time')
    country = models.CharField(max_length=300, default='India')
    state = models.CharField(max_length=300, default='Karnataka')