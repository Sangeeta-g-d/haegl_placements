from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxValueValidator
from datetime import datetime

# Create your models here.

class UploadFile(models.Model):
    excel = models.FileField(upload_to='uploads/', max_length=255)

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
    linkedin = models.CharField(max_length=400,default="xyz")


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
    J_type= models.CharField(max_length=300, default='job')


class AppliedJobs(models.Model):
    user_id = models.ForeignKey('NewUser',on_delete=models.CASCADE)
    job_id = models.ForeignKey('JobDetails',on_delete=models.CASCADE)
    experience = models.CharField(max_length=500,default='fresher')
    qualification = models.CharField(max_length=400,default='BE')
    skills = models.CharField(max_length=600,default='HTML')
    resume = models.FileField(upload_to='applied_resume/')
    applied_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=200,default='Pending')
    applied=models.BooleanField(default=False)

class CompanyJobSaved(models.Model):
    user_id=models.ForeignKey('NewUser',on_delete=models.CASCADE,related_name='UserId')
    companyIdOrAgencyId=models.ForeignKey('NewUser',on_delete=models.CASCADE,related_name='companyId')
    applied_date = models.DateField(default=timezone.now)
    job_id = models.ForeignKey('JobDetails',on_delete=models.CASCADE,default=1)


class TopCompanies(models.Model):
    company_name = models.CharField(max_length=600,default="top company")
    company_logo = models.ImageField(upload_to='uploaded_images/',default="company logo")

class InterviewQuestions(models.Model):
    company_id = models.ForeignKey('TopCompanies',on_delete=models.CASCADE)
    question = models.CharField(max_length=3000, default='question')
    answer = models.CharField(max_length=5000, default='answer')
    designation = models.CharField(max_length=300, default='none')

class UserDetails(models.Model):
    user_id = models.ForeignKey('NewUser', on_delete=models.CASCADE)
    qualification = models.CharField(max_length=300,default='BCA')
    experience = models.CharField(max_length=300,default='fresher')
    skills = models.CharField(max_length=400,default='html')
    DOB = models.CharField(max_length=100)
    about = models.CharField(max_length=1000,default='Passionate professional dedicated to driving innovation and fostering growth through collaboration and strategic expertise.')

class ContactUs(models.Model):
    
    name = models.CharField(max_length=700, default='name')
    email = models.CharField(max_length=700, default='email')
    message = models.CharField(max_length=700, default='message')
   
