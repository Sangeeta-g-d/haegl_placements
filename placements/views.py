from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden,HttpResponseBadRequest
from django.template import loader
from .models import CompanyDetails, NewUser, JobDetails, TopCompanies, InterviewQuestions, UserDetails, CompanyJobSaved, AppliedJobs, UploadFile, ContactUs,AvailableTiming, ScheduleInterview
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from datetime import datetime, timedelta
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.urls import reverse
import random
from operator import attrgetter
from django.utils import timezone
from itertools import chain
from django.core.mail import send_mail
from django.conf import settings
from urllib.parse import unquote
from django.db.models import Count
from collections import defaultdict
from django.db.models import Q
from email.mime.text import MIMEText
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from django.core.mail import send_mail
# Create your views here.


def upload_file(request):
    if request.method == 'POST':
        excel = request.FILES.get('excel')

        # Check if there is an existing file
        existing_file = UploadFile.objects.first()

        # If there is an existing file, delete it before creating a new one
        if existing_file:
            existing_file.excel.delete()  # This deletes the old file from the storage
            existing_file.excel = excel  # Replace the old file with the new one
            existing_file.save()
        else:
            # If no existing file, create a new UploadFile object with the new file
            obj = UploadFile.objects.create(excel=excel)
        return render(request, 'upload_file.html', {'message': 'Process Completed Successfully'})

    return render(request, 'upload_file.html')

def display_uploaded_file(request):
    uploaded_files = UploadFile.objects.all()
    return render(request, 'display_uploaded_file.html', {'uploaded_files': uploaded_files})

def download_file(request, file_id):
    uploaded_file = get_object_or_404(UploadFile, id=file_id)
    file_content = uploaded_file.excel.read()
    response = HttpResponse(file_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.excel.name}"'
    return response

def temp2(request):
    return render(request,'temp2.html')

def temp3(request):
    return render(request,'temp3.html')

def new_index(request):
    recent_jobs = list(JobDetails.objects.filter(J_type='job').order_by('-created_on')[:5])

    # Shuffle the list of recent jobs
    random.shuffle(recent_jobs)

    # Sort combined_jobs by the latest job posted (created_on) in descending order
    recent_jobs = sorted(recent_jobs, key=attrgetter('created_on'), reverse=True)

    for x in recent_jobs:

        days_since_posted = (timezone.now().date() - x.created_on).days
        x.days_since_posted = days_since_posted
    unique_departments_job = JobDetails.objects.filter(J_type='job').values_list('department', flat=True).distinct()
    all_unique_departments = list(set(chain( unique_departments_job)))

    open_status_count_job = (
        JobDetails.objects.filter(status='open',J_type='job')
        .values('department')
        .annotate(open_count=Count('department'))
    )


    open_jobs_count = defaultdict(int)
    for item in open_status_count_job:
        open_jobs_count[item['department']] += item['open_count']

    department_open_counts = [
        (department, open_jobs_count.get(department, 0)) for department in all_unique_departments
    ]

    context = {
        'recent_jobs': recent_jobs
    }

    return render(request,'new_index.html',context)


def new_job_des(request,id):
    
    job = JobDetails.objects.select_related('company_id').filter(id=id, status="open").first()

    context = {
        'job': job,

    }
    return render(request,'new_job_des.html',context)


def voice(request):
    return render(request,'voice.html')


def index(request):
    if request.user.is_authenticated:
            print("Hiiiiiiiiiiiiiii")
            return redirect('/user_dashboard')
    recent_jobs = list(JobDetails.objects.filter(J_type='job').order_by('-created_on')[:10])

    # Shuffle the list of recent jobs
    random.shuffle(recent_jobs)

    # Sort combined_jobs by the latest job posted (created_on) in descending order
    recent_jobs = sorted(recent_jobs, key=attrgetter('created_on'), reverse=True)

    for x in recent_jobs:

        days_since_posted = (timezone.now().date() - x.created_on).days
        x.days_since_posted = days_since_posted

    unique_departments_job = JobDetails.objects.filter(J_type='job').values_list('department', flat=True).distinct()
    all_unique_departments = list(set(chain( unique_departments_job)))

    open_status_count_job = (
        JobDetails.objects.filter(status='open',J_type='job')
        .values('department')
        .annotate(open_count=Count('department'))
    )


    open_jobs_count = defaultdict(int)
    for item in open_status_count_job:
        open_jobs_count[item['department']] += item['open_count']

    department_open_counts = [
        (department, open_jobs_count.get(department, 0)) for department in all_unique_departments
    ]

    hiring_partners = NewUser.objects.filter(user_type='Company')
    for x in hiring_partners:
        print(x)

    top_companies = TopCompanies.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        obj = ContactUs.objects.create(name=name,email=email,message=message)
        return redirect('/')

    context = {
        'recent_jobs': recent_jobs,
        'all_unique_departments': all_unique_departments,
        'department_open_counts': department_open_counts,
        'hiring_partners':hiring_partners,
        'top_companies':top_companies
    }

    return render(request, 'index.html', context)


def internship_program(request):
    return render(request,'internship_program.html')

def user_internship_program(request):
    return render(request,'user_internship_program.html')

def search_results(request):
    keyword = request.GET.get('keyword')
    job_title = request.GET.get('job_title')
    location = request.GET.get('location')
    job_type = request.GET.get('type')
    print("jobbbbbbbbbbbbbb",job_title)
    combined_results = []

    if job_title:

        job_results = JobDetails.objects.filter(
            Q(designation__icontains=job_title) |
            Q(job_description__icontains=job_title) |
            Q(department__icontains=job_title) |
            Q(location__icontains=job_title) |
            Q(mandatory_skills__icontains=job_title) |
            Q(optional_skills__icontains=job_title) |
            Q(experience__icontains=job_title) |
            Q(salary__icontains=job_title) |
            Q(qualification__icontains=job_title)
        )

        # Combine both querysets into a single result set
        combined_results = list( job_results)

    elif job_title:
        # Search by job title in the designation column
        combined_results = list(chain(
            JobDetails.objects.filter(designation__icontains=job_title,J_type='job')
        ))

    elif location:
        # Search by location in the location column
        combined_results = list(chain(
            JobDetails.objects.filter(location__icontains=location,J_type='job')
        ))

    elif job_type:
        # Search by job type in the type column
        job_results = JobDetails.objects.filter(job_type=job_type,J_type='job')
        combined_results = list( job_results)

    for job in combined_results:
        # Assuming 'posted_on' is the field in your models storing the posting date
        days_since_posted = (datetime.now().date() - job.created_on).days
        job.days_since_posted = days_since_posted



    unique_departments_job = JobDetails.objects.filter(J_type='job').values_list('department', flat=True).distinct()
    all_unique_departments = list(set(chain( unique_departments_job)))

    open_status_count_job = (
        JobDetails.objects.filter(status='open',J_type='job')
        .values('department')
        .annotate(open_count=Count('department'))
    )



    open_jobs_count = defaultdict(int)
    for item in open_status_count_job:
        open_jobs_count[item['department']] += item['open_count']



    department_open_counts = [
        (department, open_jobs_count.get(department, 0)) for department in all_unique_departments
    ]
    job_details_count = JobDetails.objects.filter(J_type='job').values('location').annotate(job_count=Count('location'))

# Count jobs in each unique location from AgencyJobDetails


# Combine the counts
    combined_counts = {}

    for job_detail in job_details_count:
        combined_counts[job_detail['location']] = combined_counts.get(job_detail['location'], 0) + job_detail['job_count']



# Print or use the job counts in each unique location as needed
    print(combined_counts)
    context = {
        'combined_results': combined_results,
        'keyword': keyword,
        'job_title': job_title,
        'location': location,
        'job_type': job_type,
        'department_open_counts':department_open_counts,
        'combined_counts':combined_counts,
    }

    return render(request, 'search_results.html', context)


def internship_search_results(request):
    keyword = request.GET.get('keyword')
    job_title = request.GET.get('job_title')
    location = request.GET.get('location')
    job_type = request.GET.get('type')

    combined_results = []

    if keyword:

        job_results = JobDetails.objects.filter(
            Q(designation__icontains=keyword) |
            Q(job_description__icontains=keyword) |
            Q(department__icontains=keyword) |
            Q(location__icontains=keyword) |
            Q(mandatory_skills__icontains=keyword) |
            Q(optional_skills__icontains=keyword) |
            Q(experience__icontains=keyword) |
            Q(salary__icontains=keyword) |
            Q(qualification__icontains=keyword)
        )

        # Combine both querysets into a single result set
        combined_results = list( job_results)

    elif job_title:
        # Search by job title in the designation column
        combined_results = list(chain(
            JobDetails.objects.filter(designation__icontains=job_title,J_type='internship')
        ))

    elif location:
        print("!!!!!!",location)
        # Search by location in the location column
        combined_results = list(chain(
            JobDetails.objects.filter(location__icontains=location,J_type='internship')
        ))

    elif job_type:
        # Search by job type in the type column
        job_results = JobDetails.objects.filter(job_type=job_type,J_type='internship')
        combined_results = list( job_results)

    for job in combined_results:
        # Assuming 'posted_on' is the field in your models storing the posting date
        days_since_posted = (datetime.now().date() - job.created_on).days
        job.days_since_posted = days_since_posted
        print(job)

# Print or use the job counts in each unique location as needed

    context = {
        'combined_results': combined_results,
        'keyword': keyword,
        'job_title': job_title,
        'location': location,
        'job_type': job_type,


    }

    return render(request, 'internship_search_results.html', context)

@login_required
def internship_search(request):
    if request.user.user_type != 'job seeker':
        return HttpResponseForbidden()
    keyword = request.GET.get('keyword')
    job_title = request.GET.get('job_title')
    location = request.GET.get('location')
    job_type = request.GET.get('type')

    combined_results = []

    if keyword:

        job_results = JobDetails.objects.filter(
            Q(designation__icontains=keyword) |
            Q(job_description__icontains=keyword) |
            Q(department__icontains=keyword) |
            Q(location__icontains=keyword) |
            Q(mandatory_skills__icontains=keyword) |
            Q(optional_skills__icontains=keyword) |
            Q(experience__icontains=keyword) |
            Q(salary__icontains=keyword) |
            Q(qualification__icontains=keyword)
        )

        # Combine both querysets into a single result set
        combined_results = list( job_results)

    elif job_title:
        # Search by job title in the designation column
        combined_results = list(chain(
            JobDetails.objects.filter(designation__icontains=job_title,J_type='internship')
        ))

    elif location:
        print("!!!!!!",location)
        # Search by location in the location column
        combined_results = list(chain(
            JobDetails.objects.filter(location__icontains=location,J_type='internship')
        ))

    elif job_type:
        # Search by job type in the type column
        job_results = JobDetails.objects.filter(job_type=job_type,J_type='internship')
        combined_results = list( job_results)

    for job in combined_results:
        # Assuming 'posted_on' is the field in your models storing the posting date
        days_since_posted = (datetime.now().date() - job.created_on).days
        job.days_since_posted = days_since_posted
        print(job)

# Print or use the job counts in each unique location as needed

    context = {
        'combined_results': combined_results,
        'keyword': keyword,
        'job_title': job_title,
        'location': location,
        'job_type': job_type,


    }

    return render(request, 'internship_search.html', context)



@login_required
def user_search_results(request):
    if request.user.user_type != 'job seeker':
        return HttpResponseForbidden()
    keyword = request.GET.get('keyword')
    job_title = request.GET.get('job_title')
    location = request.GET.get('location')
    job_type = request.GET.get('type')

    combined_results = []

    if keyword:

        job_results = JobDetails.objects.filter(
            Q(designation__icontains=keyword) |
            Q(job_description__icontains=keyword) |
            Q(department__icontains=keyword) |
            Q(location__icontains=keyword) |
            Q(mandatory_skills__icontains=keyword) |
            Q(optional_skills__icontains=keyword) |
            Q(experience__icontains=keyword) |
            Q(salary__icontains=keyword) |
            Q(qualification__icontains=keyword)
        )

        # Combine both querysets into a single result set
        combined_results = list( job_results)

    elif job_title:
        # Search by job title in the designation column
        combined_results = list(chain(
            JobDetails.objects.filter(designation__icontains=job_title,J_type='job')
        ))

    elif location:
        # Search by location in the location column
        combined_results = list(chain(
            JobDetails.objects.filter(location__icontains=location,J_type='job')
        ))

    elif job_type:
        # Search by job type in the type column
        job_results = JobDetails.objects.filter(job_type=job_type,J_type='job')
        combined_results = list(job_results)

    for job in combined_results:
        # Assuming 'posted_on' is the field in your models storing the posting date
        days_since_posted = (datetime.now().date() - job.created_on).days
        job.days_since_posted = days_since_posted



    unique_departments_job = JobDetails.objects.filter(J_type='job').values_list('department', flat=True).distinct()
    all_unique_departments = list(set(chain( unique_departments_job)))

    open_status_count_job = (
        JobDetails.objects.filter(status='open',J_type='job')
        .values('department')
        .annotate(open_count=Count('department'))
    )



    open_jobs_count = defaultdict(int)
    for item in open_status_count_job:
        open_jobs_count[item['department']] += item['open_count']



    department_open_counts = [
        (department, open_jobs_count.get(department, 0)) for department in all_unique_departments
    ]
    job_details_count = JobDetails.objects.filter(J_type='job').values('location').annotate(job_count=Count('location'))

# Count jobs in each unique location from AgencyJobDetails


# Combine the counts
    combined_counts = {}

    for job_detail in job_details_count:
        combined_counts[job_detail['location']] = combined_counts.get(job_detail['location'], 0) + job_detail['job_count']



# Print or use the job counts in each unique location as needed
    print(combined_counts)
    context = {
        'combined_results': combined_results,
        'keyword': keyword,
        'job_title': job_title,
        'location': location,
        'job_type': job_type,
        'department_open_counts':department_open_counts,
        'combined_counts':combined_counts,
    }

    return render(request, 'user_search_results.html', context)




@login_required
def admin_db(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden()
    i = request.user.id
    obj = NewUser.objects.get(id=i)
    today_date = date.today()

    data = NewUser.objects.filter(user_type='Company')
    context = {
        'obj':obj,
        'today_date':today_date,
        'data':data,
    }
    print(data)
    return render(request,'admin_db.html',context)

def delete_user(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        try:
            # Get user object by ID and delete it
            user = NewUser.objects.get(id=user_id)
            user.delete()
            return HttpResponse(status=200)  # Success response
        except NewUser.DoesNotExist:
            return HttpResponse(status=404)  # User not found
    else:
        return HttpResponse(status=405)  # Method not allowed

def update_status(request):
    print("hiiiiiiiiiiii")
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print("Hiiiiiiiiiiiiii")
        user_id = request.POST.get('user_id')
        user = get_object_or_404(NewUser, id=user_id)
        print("userrrrrrr",user)

        # Assuming 'status' is a BooleanField in your model
        user.status = True
        user.save()

        return JsonResponse({'message': 'Status updated successfully!'})
    return JsonResponse({}, status=400)

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            print(request.user)
            return redirect('/admin_db')
        else:
            messages.error(request,'Wrong Credentials')
            return redirect('/admin_login')
    return render(request,'admin_login.html')


def admin_logout(request):
    logout(request)
    # Redirect to a specific page after logout (optional)
    return redirect('/admin_login')

def approve_user(request):
    if request.method == 'POST':
        print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
        user_id = request.POST.get('user_id')
        try:
            user = NewUser.objects.get(id=user_id)
            # Update status to True (approved)
            user.status = True
            user.save()
            return JsonResponse({'status': 'success'})
        except NewUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User does not exist'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def company_logout(request):
    logout(request)
    # Redirect to a specific page after logout (optional)
    return redirect('/')

def contact_us(request): 
    return render(request,'contact_us.html')

def registration(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_no')
        address = request.POST.get('address')
        company_logo = request.FILES.get('profile')
        user_type = "Company"
        
        # Hash the password
        passw = make_password(password)
        
        # Create a new user
        user = NewUser.objects.create(
            first_name=company_name,
            username=username,
            password=passw,
            email=email,
            phone_no=contact_no,
            user_type=user_type,
            address=address,
            profile=company_logo
        )
        
        # Redirect to login page with success message in query parameter
        success_message = f"Registered successfully! Username: {username}, Password: {password}"
        return redirect(f'/login?success_message={success_message}')

    return render(request, 'registration.html')

def login1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.user_type == 'Company' and user.status == True:
            login(request, user)
            return redirect('/company_dashboard')
            
        elif user is not None and user.user_type == 'Company' and user.status == False:
            error_message = 'Wait till account verifies'
            return redirect(f'/login?error_message={error_message}')
        
        else:
            error_message = 'Account not found'
            return redirect(f'/login?error_message={error_message}')

    return render(request, 'login.html')

def add_company_details(request):
    i = request.user.id
    obj = NewUser.objects.get(id=i)

    if request.method == 'POST':
        tag_line = request.POST.get('tag_line')
        company_type = request.POST.get('company_type')
        service_sector = request.POST.get('service_sector')
        founded_year = request.POST.get('founded_year')
        head_branch = request.POST.get('head_branch')
        linkedin = request.POST.get('linkedin')
        instagram = request.POST.get('instagram')
        facebook = request.POST.get('facebook')
        website = request.POST.get('website')
        highlights = request.POST.get('highlights')
        why_us = request.POST.get('why_us')
        milestone = request.POST.get('milestone')
        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')
        cover_image = request.FILES.get('cover_image')

        obj = CompanyDetails.objects.create(company_id_id=i,tag_line=tag_line,company_type=company_type,company_service_sector=service_sector,founded_year=founded_year,
        head_branch=head_branch,linkedin_url=linkedin,instagram_url=instagram,
        facebook=facebook,webiste=website,
        Key_highlights=highlights,why_us=why_us,
        milestone=milestone,
        other_image1=img1,
        other_image2=img2,cover_image=cover_image)

        print(obj)
        return redirect('/company_dashboard')
    return render(request,'company_details.html')

@login_required
def top_companies(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden()
    data = TopCompanies.objects.all()
    context = {
        'data':data
    }
    return render(request,'top_companies.html',context )

def add_top_company(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        company_logo = request.FILES.get('company_logo')
        data = TopCompanies.objects.create(company_name=company_name,company_logo=company_logo)
        print(data)
        return redirect('/top_companies')

def add_questions(request):
    if request.method == 'POST':
        company_id = request.POST.get('companyId')
        #print(company_id)
        question = request.POST.get('question')
        #print(question)
        answer = request.POST.get('answer')
        designation = request.POST.get('designation')
        #print(answer)
        data = InterviewQuestions.objects.create(company_id_id = company_id, question=question,
        answer=answer,designation=designation)
        return redirect('/top_companies')

@login_required
def company_dashboard(request):
    if request.user.user_type != 'Company':
        return HttpResponseForbidden()
    first_name = request.user.first_name
    print(first_name)
    context = {
        'first_name':first_name
    }
    return render(request,'company_dashboard.html',context)

@login_required
def job_vacancy(request):
    if request.user.user_type != 'Company':
        return HttpResponseForbidden()
    
    success_message = request.GET.get('success_message')
    i = request.user.id
    obj = NewUser.objects.get(id=i)
    today_date = date.today()
    search_query = request.GET.get('search_query', '')
    designation_filter = request.GET.get('designation', '') 
    print("kkkkkkkkkkkkkkkk",designation_filter) 

    # Fetch distinct designations from JobDetails
    designations = JobDetails.objects.filter(company_id_id=i, J_type='job').values_list('designation', flat=True).distinct()

    data = JobDetails.objects.filter(company_id_id=i, J_type='job')

    if search_query:
        # Perform search query filtering
        data = data.filter(
            Q(designation__icontains=search_query) |
            Q(department__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(mandatory_skills__icontains=search_query) |
            Q(optional_skills__icontains=search_query) |
            Q(qualification__icontains=search_query) |
            Q(no_of_vacancy__icontains=search_query) |
            Q(experience__icontains=str(search_query)) |
            Q(salary__icontains=str(search_query))
        )
    
    if designation_filter and designation_filter != 'All':
        # Filter jobs based on selected designation
        data = data.filter(designation__icontains=designation_filter)

    context = {
        'obj': obj,
        'today_date': today_date,
        'data': data,
        'success_message': success_message,
        'first_name': request.user.first_name,
        'designations': ['All'] + list(designations)  # Add 'All' option to designations list
    }

    return render(request, 'job_vacancy.html', context)

@login_required
def internship_list(request):
    if request.user.user_type != 'Company':
        return HttpResponseForbidden()
    success_message = request.GET.get('success_message')
    i = request.user.id
    obj = NewUser.objects.get(id=i)
    today_date = date.today()
    search_query = request.GET.get('search_query', '')
    designation_filter = request.GET.get('designation', '') 
    print("kkkkkkkkkkkkkkkk",designation_filter) 

    # Fetch distinct designations from JobDetails
    designations = JobDetails.objects.filter(company_id_id=i, J_type='internship').values_list('designation', flat=True).distinct()

    data = JobDetails.objects.filter(company_id_id=i, J_type='internship')

    if search_query:
        # Perform search query filtering
        data = data.filter(
            Q(designation__icontains=search_query) |
            Q(department__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(mandatory_skills__icontains=search_query) |
            Q(optional_skills__icontains=search_query) |
            Q(qualification__icontains=search_query) |
            Q(no_of_vacancy__icontains=search_query) |
            Q(experience__icontains=str(search_query)) |
            Q(salary__icontains=str(search_query))
        )
    
    if designation_filter and designation_filter != 'All':
        # Filter jobs based on selected designation
        data = data.filter(designation__icontains=designation_filter)

    context = {
        'obj': obj,
        'today_date': today_date,
        'data': data,
        'success_message': success_message,
        'first_name': request.user.first_name,
        'designations': ['All'] + list(designations)  # Add 'All' option to designations list
    }

    return render(request,'internship_list.html',context)


def toggle_status(request, job_id):
    print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    # Implement logic to toggle the status for the job with the given ID
    job = JobDetails.objects.get(id=job_id)
    job.status = 'closed' if job.status == 'open' else 'open'
    job.save()

    # Return the new status as JSON
    return JsonResponse({'newStatus': job.status})

def delete_job(request, job_id):
    if request.method == 'DELETE':
        try:
            job = JobDetails.objects.get(id=job_id)
            job.delete()
            return JsonResponse({'message': 'Job deleted successfully'}, status=200)
        except Job.DoesNotExist:
            return JsonResponse({'error': 'Job does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def add_job(request):
    i = request.user.id
    obj = NewUser.objects.get(id=i)
    first_name = request.user.first_name
    today_date = date.today()
    context = {'obj':obj,'today_date':today_date,'first_name':first_name}
    if request.method == 'POST':
        designation = request.POST.get('designation')
        department = request.POST.get('department')
        location = request.POST.get('location')
        work_mode = request.POST.get('work_mode')
        no_of_vacancy = request.POST.get('no_of_vacancy')
        mandatory_skills = request.POST.get('mandatory_skills')
        optional_skills = request.POST.get('optional_skills')
        experience = request.POST.get('experience')
        qualification = request.POST.get('qualification')
        salary = request.POST.get('package')
        status = request.POST.get('status')
        job_type = request.POST.get('job_type')
        description = request.POST.get('job_description')
        state = request.POST.get('state')
        type = request.POST.get('type')
        country = request.POST.get('country')
        is_promoting = request.POST.get('is_promoting')
        job_link = request.POST.get('job_link')
        company_profile = request.FILES.get('company_profile')
        company_name = request.POST.get('company_name')


        obj = JobDetails.objects.create(company_id_id=i,designation=designation,department=department,location=location,work_mode=work_mode,
        no_of_vacancy=no_of_vacancy,mandatory_skills=mandatory_skills,optional_skills=optional_skills,
        qualification=qualification,experience=experience,
        salary=salary,job_description=description,J_type=type,
        is_promoting=is_promoting,job_link=job_link,company_profile=company_profile,promoting_company_name=company_name,job_type=job_type)

        print(obj)
        return redirect(reverse('job_vacancy') + '?success_message=1')

    return render(request,'add_job.html',context)


def add_internship(request):
    i = request.user.id
    obj = NewUser.objects.get(id=i)
    first_name = request.user.first_name
    today_date = date.today()
    context = {'obj':obj,'today_date':today_date,'first_name':first_name}
    if request.method == 'POST':
        designation = request.POST.get('designation')
        department = request.POST.get('department')
        location = request.POST.get('location')
        work_mode = request.POST.get('work_mode')
        no_of_vacancy = request.POST.get('no_of_vacancy')
        mandatory_skills = request.POST.get('mandatory_skills')
        optional_skills = request.POST.get('optional_skills')
        experience = request.POST.get('experience')
        qualification = request.POST.get('qualification')
        salary = request.POST.get('package')
        status = request.POST.get('status')
        description = request.POST.get('job_description')
        state = request.POST.get('state')
        country = request.POST.get('country')
        type = request.POST.get('type')
        obj = JobDetails.objects.create(company_id_id=i,designation=designation,department=department,location=location,work_mode=work_mode,
        no_of_vacancy=no_of_vacancy,mandatory_skills=mandatory_skills,optional_skills=optional_skills,
        qualification=qualification,experience=experience,
        salary=salary,job_description=description,J_type=type)

        print(obj)
        return redirect(reverse('internship_list') + '?success_message=1')

    return render(request,'add_internship.html',context)


def user_registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        linkedin = request.POST.get('linkedin')
        
        # Check if the username already exists
        if NewUser.objects.filter(username=username).exists():
            return render(request, 'user_registration.html', {'username_exists': True})
        
        if NewUser.objects.filter(phone_no=phone_no).exists():
            return render(request, 'user_registration.html', {'phone_no_exists': True})
        
        # Check if the email already exists
        if NewUser.objects.filter(email=email).exists():
            return render(request, 'user_registration.html', {'email_exists': True})

        passw = make_password(password)
        
        user = NewUser.objects.create(username=username, password=passw,
                                       email=email, phone_no=phone_no, linkedin=linkedin)
        
        return render(request, 'user_registration.html', {'registered': True})
    
    return render(request, 'user_registration.html')


def select_theme(request):
    return render(request,'select_theme.html')

def user_select_theme(request):
    return render(request,'user_select_theme.html')

def temp1(request):
    return render(request,'temp1.html')

def company_calendar(request):
    first_name = request.user.first_name
    company_id = request.user.id
    data = ScheduleInterview.objects.select_related('application_id','user_id').filter(application_id_id__job_id_id__company_id = company_id)
    print("jjjjjjjjjjjj",data)
    context = {
        'first_name':first_name,'data':data
    }
    return render(request,'company_calendar.html',context)

def fetch_scheduled_dates(request):
    scheduled_dates = ScheduleInterview.objects.values_list('interview_date', flat=True)
    print(scheduled_dates)
    return JsonResponse({'scheduled_dates': list(scheduled_dates)})

def get_scheduled_interviews(request):
    company_id = request.user.id
    if request.method == 'GET' and 'date' in request.GET:
        date_str = request.GET.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d')
        date += timedelta(days=1)  # Add one day
        next_day_str = date.strftime('%Y-%m-%d')
        scheduled_interviews = ScheduleInterview.objects.select_related('user_id', 'application_id').filter(interview_date=next_day_str, application_id_id__job_id_id__company_id=company_id)

        interviews_list = []
        for interview in scheduled_interviews:
            interview_info = {
                'scheduled_id':interview.id,
                'designation': interview.application_id.job_id.designation,
                'date': interview.interview_date,
                'start_time': interview.start_time,
                'end_time': interview.end_time,
                'mode_of_interview': interview.mode_of_interview,
                'user_name': interview.user_id.first_name,
                'user_email': interview.user_id.email
            }
            interviews_list.append(interview_info)

        return JsonResponse({'interviews': interviews_list})
    else:
        return JsonResponse({'error': 'Invalid request'})




def reschedule_interview(request, scheduled_id):
    if request.method == 'POST':
        # Retrieve form data
        new_date = request.POST.get('new_date')
        new_start_time = request.POST.get('new_start_time')
        new_end_time = request.POST.get('new_end_time')
        new_mode_of_interview = request.POST.get('new_mode_of_interview')

        try:
            scheduled_interview = ScheduleInterview.objects.get(id=scheduled_id)
            user_id = scheduled_interview.user_id_id
            data = NewUser.objects.get(id=user_id)
            user_email = data.email
            print(user_email)
            old_date = scheduled_interview.interview_date
            old_start_time = scheduled_interview.start_time
            old_end_time = scheduled_interview.end_time
            old_mode_of_interview = scheduled_interview.mode_of_interview
            print("hhhhhhhhhhhhhhhhhhh")
            # Update the scheduled interview with new details
            scheduled_interview.interview_date = new_date
            scheduled_interview.start_time = new_start_time
            scheduled_interview.end_time = new_end_time
            scheduled_interview.mode_of_interview = new_mode_of_interview
            scheduled_interview.save()
            print("llllllllllllllllllll")
            # Prepare email content
            subject = 'Interview Rescheduled'
            body = f"Your interview scheduled for {old_date} from {old_start_time} to {old_end_time} ({old_mode_of_interview}) has been rescheduled to {new_date} from {new_start_time} to {new_end_time} ({new_mode_of_interview})."
            user_email=user_email
            sender_email = settings.EMAIL_HOST_USER
            print("iiiiiiiiiiiiiiiiiiiiiii")
            # Send email
            send_mail(subject, body, sender_email, [user_email])
            print("Rescheduled interview email sent successfully")

            return JsonResponse({'status': 'success', 'message': 'Interview rescheduled successfully'})
        except ScheduleInterview.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Scheduled interview not found'}, status=404)
        except NewUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    else:
        # Handle GET request if needed (e.g., render form for rescheduling)
        pass

            


def save_available_timings(request):
    company_id = request.user.id
    print("xcv bnmfvgbhnm")
    if request.method == 'POST':
        selected_date = request.POST.get('selectedDate')
        start_time = request.POST.get('startTime')
        end_time = request.POST.get('endTime')
        # Create and save SelectedTiming object
        selected_timing = AvailableTiming(date=selected_date, start_time=start_time, end_time=end_time,company_id_id=company_id)
        selected_timing.save()

        return JsonResponse({'message': 'Data saved successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_available_timings(request):
    print("hiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    company_id = request.user.id
    available_timings = AvailableTiming.objects.filter(company_id_id=company_id).values('date', 'start_time', 'end_time')
    return JsonResponse(list(available_timings), safe=False)

def user_login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        print("Username or Email:", username_or_email)
        password = request.POST.get('password')
        print("Password:", password)

        user = authenticate(request, username=username_or_email, password=password)
        print("Authenticated User:", user)

        if user is not None:
            login(request, user)
            return redirect('/jobs')
        else:
            error_message = "Invalid username/email or password."
            return render(request, 'user_login.html', {'error_message': error_message})

    return render(request, 'user_login.html')

def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)

def search_trend(request, keyword):
    print(keyword)
    if keyword == 'freshers':
        job_details = JobDetails.objects.filter(
            Q(experience='Fresher') | Q(experience__startswith='0-'),
            status='open',J_type='job'
        )

    elif keyword == 'internship':
        job_details = JobDetails.objects.filter(
            Q(J_type='internship'),
            status='open'
        )

    elif keyword == 'sales':
        job_details = JobDetails.objects.filter(
            Q(department='Sales and Marketing'),
            status='open',J_type='job'
        )

    else:
        job_details = JobDetails.objects.filter(
            Q(department='Research and Development') | Q(department='Information Technology (IT)') ,
            status='open',J_type='job'
        )

    all_jobs = list(chain(job_details))
    print(all_jobs)

    for job in all_jobs:
        today = datetime.now().date()  # Define 'today' here for each iteration
        days_posted_ago = (today - job.created_on).days
        job.days_posted_ago = days_posted_ago

    # Sort the combined queryset based on days posted (latest at the top)
    job_details = sorted(all_jobs, key=lambda x: x.created_on, reverse=True)
    #print("^^^^^^^^^^^^^",all_jobs)

    unique_departments_job = JobDetails.objects.filter(J_type='job').values_list('department', flat=True).distinct()
    all_unique_departments = list(set(chain( unique_departments_job)))

    open_status_count_job = (
        JobDetails.objects.filter(status='open',J_type='job')
        .values('department')
        .annotate(open_count=Count('department'))
    )

    open_jobs_count = defaultdict(int)
    for item in open_status_count_job:
        open_jobs_count[item['department']] += item['open_count']



    department_open_counts = [
        (department, open_jobs_count.get(department, 0)) for department in all_unique_departments
    ]

    job_details_count = JobDetails.objects.filter(J_type='job').values('location').annotate(job_count=Count('location'))

# Count jobs in each unique location from AgencyJobDetails


# Combine the counts
    combined_counts = {}

    for job_detail in job_details_count:
        combined_counts[job_detail['location']] = combined_counts.get(job_detail['location'], 0) + job_detail['job_count']

    context = {
        'all_jobs': all_jobs,
        'department_open_counts':department_open_counts,
        'combined_counts':combined_counts,'keyword':keyword,
    }
    return render(request,'search_trend.html', context)

def single_job(request, job_id):
    id = request.user.id
    job = JobDetails.objects.select_related('company_id').filter(id=job_id, status="open").first()
    data = NewUser.objects.filter(id=id).first()
    
    # Extract individual keywords from the current job
    keywords = job.mandatory_skills.split(',')  # Assuming keywords are comma-separated
    
    # Get similar jobs based on shared mandatory skills
    similar_jobs = []
    for keyword in keywords:
        similar_jobs.extend(JobDetails.objects.filter(mandatory_skills__icontains=keyword.strip(), status="open").select_related('company_id').exclude(id=job_id))
    
    # Remove duplicates from similar_jobs list
    similar_jobs = list(set(similar_jobs))
    print("similarrrrrrrrrrrr",similar_jobs)
    for x in similar_jobs:
        print(x.company_id.profile)
    context = {
        'job': job,
        'data': data,
        'similar_jobs': similar_jobs
    }

    return render(request, 'single_job.html', context)

def user_single_job(request, job_id):
    id = request.user.id
    job = JobDetails.objects.select_related('company_id').filter(id=job_id, status="open").first()
    
    data = NewUser.objects.filter(id=id).first()
    print(data)
    obj = UserDetails.objects.filter(user_id_id=id).first()
    print(obj)
    # Extract individual keywords from the current job
    keywords = job.mandatory_skills.split(',')  # Assuming keywords are comma-separated
    
    applied = AppliedJobs.objects.filter(user_id=id, job_id=job_id).exists()
    # Get similar jobs based on shared mandatory skills
    similar_jobs = []
    for keyword in keywords:
        similar_jobs.extend(JobDetails.objects.filter(mandatory_skills__icontains=keyword.strip(), status="open").select_related('company_id').exclude(id=job_id))
    
    # Remove duplicates from similar_jobs list
    similar_jobs = list(set(similar_jobs))
    print("similarrrrrrrrrrrr",similar_jobs)
    for x in similar_jobs:
        print(x.company_id.profile)
    context = {
        'job': job,
        'data': data,
        'similar_jobs': similar_jobs,
        'obj':obj,'applied':applied
    }

    return render(request, 'user_single_job.html', context)

def company(request,id):
    print("iddddddddd",id)
    obj = NewUser.objects.get(id=id)
    info = CompanyDetails.objects.filter(company_id_id=id).first()
    c_img = info.cover_image
    print(info.other_image1)
    print("LinkedIn URL:", info.linkedin_url)
    company_names = []
    company_jobs_dict = {}

    if obj.user_type == 'Company':
        # If the user is a company, retrieve jobs related to that company
        jobs = JobDetails.objects.filter(company_id_id=id,J_type='job')
        company_names = [obj.first_name]
        display_jobs = JobDetails.objects.filter(company_id_id=id,J_type='job')  # Assuming company_name exists in the NewUser model
        # Additional logic for companies if needed

    context = {
        'jobs': jobs,
        'company_names': company_names,
        'company_jobs_dict': company_jobs_dict,
        'obj': obj,
        'info':info,
        'c_img':c_img,
        'display_jobs':display_jobs

    }
    return render(request,'company.html',context)


def job_list(request, department):
    print(department)
    decoded_department = unquote(department)
    print("!!!!!!!!!!",decoded_department)
    job_details = JobDetails.objects.filter(department=decoded_department, status='open',J_type='job')
    print("##########",job_details)

    all_jobs = list(chain(job_details))
    for job in all_jobs:
        today = datetime.now().date()  # Define 'today' here for each iteration
        days_posted_ago = (today - job.created_on).days
        job.days_posted_ago = days_posted_ago

    # Sort the combined queryset based on days posted (latest at the top)
    all_jobs = sorted(all_jobs, key=lambda x: x.created_on, reverse=True)


    unique_departments_job = JobDetails.objects.filter(J_type='job').values_list('department', flat=True).distinct()
    all_unique_departments = list(set(chain( unique_departments_job)))

    open_status_count_job = (
        JobDetails.objects.filter(status='open',J_type='job')
        .values('department')
        .annotate(open_count=Count('department'))
    )



    open_jobs_count = defaultdict(int)
    for item in open_status_count_job:
        open_jobs_count[item['department']] += item['open_count']



    department_open_counts = [
        (department, open_jobs_count.get(department, 0)) for department in all_unique_departments
    ]


    job_details_count = JobDetails.objects.filter(J_type='job').values('location').annotate(job_count=Count('location'))

# Count jobs in each unique location from AgencyJobDetails


# Combine the counts
    combined_counts = {}

    for job_detail in job_details_count:
        combined_counts[job_detail['location']] = combined_counts.get(job_detail['location'], 0) + job_detail['job_count']



    context = {
        'all_jobs': all_jobs,
        'selected_department': decoded_department,
        'department_open_counts':department_open_counts,

        'combined_counts':combined_counts
    }

    return render(request, 'job_list.html', context)

@login_required
def user_job_list(request, department):
    if request.user.user_type != 'job seeker':
        return HttpResponseForbidden()
    print(department)
    decoded_department = unquote(department)
    print("!!!!!!!!!!",decoded_department)
    job_details = JobDetails.objects.filter(department=decoded_department, status='open',J_type='job')
    print("##########",job_details)

    all_jobs = list(chain(job_details))
    for job in all_jobs:
        today = datetime.now().date()  # Define 'today' here for each iteration
        days_posted_ago = (today - job.created_on).days
        job.days_posted_ago = days_posted_ago

    # Sort the combined queryset based on days posted (latest at the top)
    all_jobs = sorted(all_jobs, key=lambda x: x.created_on, reverse=True)


    unique_departments_job = JobDetails.objects.filter(J_type='job').values_list('department', flat=True).distinct()
    all_unique_departments = list(set(chain( unique_departments_job)))

    open_status_count_job = (
        JobDetails.objects.filter(status='open',J_type='job')
        .values('department')
        .annotate(open_count=Count('department'))
    )



    open_jobs_count = defaultdict(int)
    for item in open_status_count_job:
        open_jobs_count[item['department']] += item['open_count']



    department_open_counts = [
        (department, open_jobs_count.get(department, 0)) for department in all_unique_departments
    ]


    job_details_count = JobDetails.objects.filter(J_type='job').values('location').annotate(job_count=Count('location'))
    saved_company_jobs_ids = CompanyJobSaved.objects.filter(user_id=request.user.id).values_list('job_id_id', flat=True)
    saved_job_ids =  list(saved_company_jobs_ids)

# Count jobs in each unique location from AgencyJobDetails


# Combine the counts
    combined_counts = {}

    for job_detail in job_details_count:
        combined_counts[job_detail['location']] = combined_counts.get(job_detail['location'], 0) + job_detail['job_count']



    context = {
        'all_jobs': all_jobs,
        'selected_department': decoded_department,
        'department_open_counts':department_open_counts,

        'combined_counts':combined_counts
    }

    return render(request, 'user_job_list.html', context)



def all_companies(request):
    hiring_partners = NewUser.objects.filter(user_type='Company')
    context = {
    'hiring_partners':hiring_partners
    }
    return render(request,'all_companies.html',context)


def all_jobs(request, category=None):
    print("cccccccccccccc", category)
    data = JobDetails.objects.all().select_related('company_id').filter(status="open", J_type='job').order_by('created_on')
    print(data)

    if category:
        print("categorryyyyyyyyyyyyyyy")
        category = category.replace('+', ' ')
        data = data.filter(department=category)

    combined_data = list(chain(data))
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^", combined_data)

    # Shuffle the combined list
    random.shuffle(combined_data)

    # Sort the combined list based on 'created_on' attribute to display recent jobs first
    combined_data.sort(key=lambda x: x.created_on, reverse=True)

    paginator = Paginator(combined_data, 12)  # 12 jobs per page
    page_number = request.GET.get('page')
    try:
        jobs_page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        jobs_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        jobs_page = paginator.page(paginator.num_pages)

    for x in jobs_page:
        days_since_posted = (timezone.now().date() - x.created_on).days
        x.days_since_posted = days_since_posted

    unique_departments = JobDetails.objects.values('department').annotate(count=Count('department')).order_by('department')

    for department in unique_departments:
        print(f"Department: {department['department']} - Count: {department['count']}")

    unique_locations = JobDetails.objects.values('location').annotate(count=Count('location')).order_by('location')

    context = {
        'data': data,
        'combined_data': combined_data,
        'unique_departments': unique_departments,
        'unique_locations': unique_locations,
        'jobs_page': jobs_page
    }
    return render(request, 'all_jobs.html', context)


@login_required
def jobs(request, category=None):
    if request.user.user_type != 'job seeker':
        return HttpResponseForbidden()
    print("cccccccccccccc", category)
    data = JobDetails.objects.all().select_related('company_id').filter(status="open", J_type='job').order_by('created_on')
    print(data)

    if category:
        print("categorryyyyyyyyyyyyyyy")
        category = category.replace('+', ' ')
        data = data.filter(department=category)

    combined_data = list(chain(data))
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^", combined_data)

    # Shuffle the combined list
    random.shuffle(combined_data)

    # Sort the combined list based on 'created_on' attribute to display recent jobs first
   
    paginator = Paginator(combined_data, 12)  # 12 jobs per page
    page_number = request.GET.get('page')
    try:
        jobs_page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        jobs_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        jobs_page = paginator.page(paginator.num_pages)

    for x in jobs_page:
        days_since_posted = (timezone.now().date() - x.created_on).days
        x.days_since_posted = days_since_posted

    unique_departments = JobDetails.objects.values('department').annotate(count=Count('department')).order_by('department')

    for department in unique_departments:
        print(f"Department: {department['department']} - Count: {department['count']}")

    unique_locations = JobDetails.objects.values('location').annotate(count=Count('location')).order_by('location')

    context = {
        'data': data,
        'combined_data': combined_data,
        'unique_departments': unique_departments,
        'unique_locations': unique_locations,
        'jobs_page': jobs_page
    }
    return render(request,'jobs.html',context)

from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def save_job(request, job_id, u_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        job_id = data.get('job_id')
        u_id = data.get('u_id')

        # Fetch user and company/agency based on IDs (Replace this logic as per your actual implementation)
        user_id = request.user.id

        # Replace '1' with your logic to fetch the user
        # Replace this with your logic
        duplicate = CompanyJobSaved.objects.filter(job_id_id = job_id, companyIdOrAgencyId_id=u_id)
        if duplicate:
            duplicate.user_id_id=user_id
            duplicate.companyIdOrAgencyId_id=u_id
            duplicate.job_id_id=job_id
            duplicate.save()
        else:
            saved_job = CompanyJobSaved.objects.create(
                user_id_id=user_id,
                companyIdOrAgencyId_id=u_id,
                job_id_id=job_id
        )
        return JsonResponse({'message': 'Job saved successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def remove_job(request, job_id, u_id):
    print("$$$$$$",job_id,u_id)
    if request.method == 'POST':
        # Fetch user ID (You may have a different way of retrieving the user ID)
        user_id = request.user.id

        # Check if the job exists in the saved jobs of the user
        try:
            CompanyJobSaved.objects.filter(user_id_id=user_id, companyIdOrAgencyId_id=u_id, job_id_id=job_id).exists()
            saved_job = CompanyJobSaved.objects.get(user_id_id=user_id, companyIdOrAgencyId_id=u_id, job_id_id=job_id)
            saved_job.delete()
            return JsonResponse({'message': 'Job removed successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



def work_mode(request, selected_work_mode):
    print("!!!!!!!",selected_work_mode)
    selected_work_mode = selected_work_mode.replace('_', ' ')
    # Fetch jobs from AgencyJobDetails for the selected work_mode
    # Fetch jobs from JobDetails for the selected work_mode
    jobs = JobDetails.objects.filter(work_mode=selected_work_mode,J_type='job')
    print("company_job",jobs)
    # Combine both sets of jobs
    combined_jobs =  list(jobs)
    combined_jobs.sort(key=lambda x: x.created_on, reverse=True)
    print("**********",combined_jobs)


    unique_departments_job = JobDetails.objects.filter(J_type='job').values_list('department', flat=True).distinct()
    all_unique_departments = list(set(chain(unique_departments_job)))

    open_status_count_job = (
        JobDetails.objects.filter(status='open',J_type='job')
        .values('department')
        .annotate(open_count=Count('department'))
    )



    open_jobs_count = defaultdict(int)
    for item in open_status_count_job:
        open_jobs_count[item['department']] += item['open_count']



    department_open_counts = [
        (department, open_jobs_count.get(department, 0)) for department in all_unique_departments
    ]
    for job in combined_jobs:
        today = datetime.now().date()  # Define 'today' here for each iteration
        days_posted_ago = (today - job.created_on).days
        job.days_posted_ago = days_posted_ago
    job_details_count = JobDetails.objects.filter(J_type='job').values('location').annotate(job_count=Count('location'))

# Count jobs in each unique location from AgencyJobDetails


# Combine the counts
    combined_counts = {}

    for job_detail in job_details_count:
        combined_counts[job_detail['location']] = combined_counts.get(job_detail['location'], 0) + job_detail['job_count']

    context = {
        'selected_work_mode': selected_work_mode,
        'jobs': combined_jobs,
        'department_open_counts':department_open_counts,
        'selected_work_mode':selected_work_mode,
        'combined_counts':combined_counts
    }

    return render(request, 'work_mode.html', context)

@login_required
def user_work_mode(request, selected_work_mode):
    if request.user.user_type != 'job seeker':
        return HttpResponseForbidden()
    print("!!!!!!!",selected_work_mode)
    selected_work_mode = selected_work_mode.replace('_', ' ')
    # Fetch jobs from AgencyJobDetails for the selected work_mode
    # Fetch jobs from JobDetails for the selected work_mode
    jobs = JobDetails.objects.filter(work_mode=selected_work_mode)
    print("company_job",jobs)
    # Combine both sets of jobs
    combined_jobs =  list(jobs)
    combined_jobs.sort(key=lambda x: x.created_on, reverse=True)
    print("**********",combined_jobs)


    unique_departments_job = JobDetails.objects.filter(J_type='job').values_list('department', flat=True).distinct()
    all_unique_departments = list(set(chain(unique_departments_job)))

    open_status_count_job = (
        JobDetails.objects.filter(status='open',J_type='job')
        .values('department')
        .annotate(open_count=Count('department'))
    )



    open_jobs_count = defaultdict(int)
    for item in open_status_count_job:
        open_jobs_count[item['department']] += item['open_count']



    department_open_counts = [
        (department, open_jobs_count.get(department, 0)) for department in all_unique_departments
    ]
    for job in combined_jobs:
        today = datetime.now().date()  # Define 'today' here for each iteration
        days_posted_ago = (today - job.created_on).days
        job.days_posted_ago = days_posted_ago
    job_details_count = JobDetails.objects.filter(J_type='job').values('location').annotate(job_count=Count('location'))

# Count jobs in each unique location from AgencyJobDetails


# Combine the counts
    combined_counts = {}

    for job_detail in job_details_count:
        combined_counts[job_detail['location']] = combined_counts.get(job_detail['location'], 0) + job_detail['job_count']

    context = {
        'selected_work_mode': selected_work_mode,
        'jobs': combined_jobs,
        'department_open_counts':department_open_counts,
        'selected_work_mode':selected_work_mode,
        'combined_counts':combined_counts
    }

    return render(request, 'user_work_mode.html', context)

def location_related_jobs(request, location):
    print(location)
    decoded_department = unquote(location)
    job_details = JobDetails.objects.filter(location=decoded_department, status='open',J_type='job')
    print("##########",job_details)

    all_jobs = list(chain(job_details))
    for job in all_jobs:
        today = datetime.now().date()  # Define 'today' here for each iteration
        days_posted_ago = (today - job.created_on).days
        job.days_posted_ago = days_posted_ago

    # Sort the combined queryset based on days posted (latest at the top)
    all_jobs = sorted(all_jobs, key=lambda x: x.created_on, reverse=True)


    unique_departments_job = JobDetails.objects.filter(J_type='job').values_list('department', flat=True).distinct()
    all_unique_departments = list(set(chain( unique_departments_job)))

    open_status_count_job = (
        JobDetails.objects.filter(status='open',J_type='job')
        .values('department')
        .annotate(open_count=Count('department'))
    )


    open_jobs_count = defaultdict(int)
    for item in open_status_count_job:
        open_jobs_count[item['department']] += item['open_count']



    department_open_counts = [
        (department, open_jobs_count.get(department, 0)) for department in all_unique_departments
    ]


    job_details_count = JobDetails.objects.filter(J_type='job').values('location').annotate(job_count=Count('location'))

# Count jobs in each unique location from AgencyJobDetails

# Combine the counts
    combined_counts = {}

    for job_detail in job_details_count:
        combined_counts[job_detail['location']] = combined_counts.get(job_detail['location'], 0) + job_detail['job_count']



    context = {
        'all_jobs': all_jobs,
        'selected_department': decoded_department,
        'department_open_counts':department_open_counts,

        'combined_counts':combined_counts,
    }

    return render(request, 'location_related_jobs.html', context)
@login_required
def user_location_related(request, location):
    if request.user.user_type != 'job seeker':
        return HttpResponseForbidden()
    print(location)
    decoded_department = unquote(location)
    job_details = JobDetails.objects.filter(location=decoded_department, status='open',J_type='job')
    print("##########",job_details)

    all_jobs = list(chain(job_details))
    for job in all_jobs:
        today = datetime.now().date()  # Define 'today' here for each iteration
        days_posted_ago = (today - job.created_on).days
        job.days_posted_ago = days_posted_ago

    # Sort the combined queryset based on days posted (latest at the top)
    all_jobs = sorted(all_jobs, key=lambda x: x.created_on, reverse=True)


    unique_departments_job = JobDetails.objects.filter(J_type='job').values_list('department', flat=True).distinct()
    all_unique_departments = list(set(chain( unique_departments_job)))

    open_status_count_job = (
        JobDetails.objects.filter(status='open',J_type='job')
        .values('department')
        .annotate(open_count=Count('department'))
    )


    open_jobs_count = defaultdict(int)
    for item in open_status_count_job:
        open_jobs_count[item['department']] += item['open_count']



    department_open_counts = [
        (department, open_jobs_count.get(department, 0)) for department in all_unique_departments
    ]


    job_details_count = JobDetails.objects.filter(J_type='job').values('location').annotate(job_count=Count('location'))

# Count jobs in each unique location from AgencyJobDetails

# Combine the counts
    combined_counts = {}

    for job_detail in job_details_count:
        combined_counts[job_detail['location']] = combined_counts.get(job_detail['location'], 0) + job_detail['job_count']



    context = {
        'all_jobs': all_jobs,
        'selected_department': decoded_department,
        'department_open_counts':department_open_counts,

        'combined_counts':combined_counts,
    }

    return render(request, 'user_location_related.html', context)

def autocomplete_job_title_suggestions(request):
    keyword = request.GET.get('keyword')
    suggestions = set()  # Using a set to maintain unique values

    if keyword:

        job_results = JobDetails.objects.filter(
            designation__icontains=keyword,J_type='job'
        ).values_list('designation', flat=True)[:10]  # Limit suggestions to 10


        suggestions.update(job_results)

    return JsonResponse({'suggestions': list(suggestions)})

def autocomplete_internship_title_suggestions(request):
    keyword = request.GET.get('keyword')
    suggestions = set()  # Using a set to maintain unique values

    if keyword:

        job_results = JobDetails.objects.filter(
            designation__icontains=keyword,J_type='internship'
        ).values_list('designation', flat=True)[:10]  # Limit suggestions to 10


        suggestions.update(job_results)
        print(suggestions)

    return JsonResponse({'suggestions': list(suggestions)})

def questions(request,id):
    obj = TopCompanies.objects.all()
    data = InterviewQuestions.objects.select_related('company_id').filter(company_id_id=id)
    company = TopCompanies.objects.filter(id=id).first()
    company_name = company.company_name
    unique_designations = InterviewQuestions.objects.filter(company_id_id=id).exclude(designation='none').values('designation').annotate(count=Count('designation')).order_by('designation')
    print(unique_designations)
    context = {
        'obj':obj,
        'unique_designations':unique_designations,
        'company_name':company_name,
        'data':data
    }
    return render(request, 'questions.html',context)

from django.views.decorators.http import require_GET
@require_GET
def designation_questions(request):
    designation = request.GET.get('designation', '')
    company_name = request.GET.get('company_name', '')
    print("&&&&&&&",designation)

    # Query the database for InterviewQuestions based on the selected designation
    interview_data = InterviewQuestions.objects.filter(designation=designation, company_id__company_name=company_name).values()

    # Convert queryset to a list for JSON serialization
    interview_data_list = list(interview_data)

    return JsonResponse(interview_data_list, safe=False)

def user_details(request):
    id = request.user.id
    if request.method == 'POST':
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        dob = request.POST.get('dob')
        skills = request.POST.get('skills')
        obj = UserDetails.objects.create(user_id_id=id,qualification=qualification,experience=experience,DOB=dob,
        skills=skills)
        return redirect('user_dashboard')
    return render(request,'user_details.html')

@login_required
def user_dashboard1(request):
    if request.user.user_type != 'job seeker':
        return HttpResponseForbidden()
    id = request.user.id
    obj = NewUser.objects.get(id=id)

    print("profileeee",obj.profile)

    # latest jobs
    recent_jobs = list(JobDetails.objects.filter(J_type='job').order_by('-created_on')[:5])

    # Shuffle the list of recent jobs
    random.shuffle(recent_jobs)

    # Sort combined_jobs by the latest job posted (created_on) in descending order
    recent_jobs = sorted(recent_jobs, key=attrgetter('created_on'), reverse=True)

    for x in recent_jobs:

        days_since_posted = (timezone.now().date() - x.created_on).days
        x.days_since_posted = days_since_posted

    # Get user details
    user_details = UserDetails.objects.filter(user_id_id=id).first()

    # Extract user skills
    # Assuming skills are comma-separated

    # Get all job details from JobDetails model
    all_jobs = JobDetails.objects.all().select_related('company_id').filter(status="open",J_type='job')

    recommended_jobs_job_details = []

    # Compare user skills with job required skills in JobDetails model
    
    # Fetch saved job IDs for the current user from both models

    saved_company_jobs_ids = CompanyJobSaved.objects.filter(user_id=request.user.id).values_list('job_id_id', flat=True)
    saved_job_ids =  list(saved_company_jobs_ids)

   

    unique_departments_job = JobDetails.objects.filter(J_type='job').values_list('department', flat=True).distinct()
    all_unique_departments = list(set(chain( unique_departments_job)))

    open_status_count_job = (
        JobDetails.objects.filter(status='open',J_type='job')
        .values('department')
        .annotate(open_count=Count('department'))
    )


    open_jobs_count = defaultdict(int)
    for item in open_status_count_job:
        open_jobs_count[item['department']] += item['open_count']



    department_open_counts = [
        (department, open_jobs_count.get(department, 0)) for department in all_unique_departments
    ]

    job_details_count = JobDetails.objects.filter(J_type='job').values('location').annotate(job_count=Count('location'))

# Count jobs in each unique location from AgencyJobDetails


# Combine the counts
    combined_counts = {}

    for job_detail in job_details_count:
        combined_counts[job_detail['location']] = combined_counts.get(job_detail['location'], 0) + job_detail['job_count']



    context = {'obj':obj
    ,'department_open_counts':department_open_counts,
    'combined_counts':combined_counts,'recent_jobs':recent_jobs
    }
    return render(request,'user_dashboard.html',context)

def application(request, job_id):
    id = request.user.id
    obj = NewUser.objects.get(id=id)
    today_date = date.today()
    user_id = AppliedJobs.objects.filter(user_id_id=id)
    degree = UserDetails.objects.filter(user_id_id=id).values('qualification')
    
    if request.method == 'POST':
        skills = request.POST.get('skills')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        expected_salary = request.POST.get('expected_salary')
        resume = request.FILES.get('resume')
        
        application = AppliedJobs.objects.create(
            user_id_id=id,
            job_id_id=job_id,
            skills=skills,
            qualification=degree,  # Use degree directly as qualification
            experience=experience,
            resume=resume,
            applied=True
        )

        # Return a JSON response indicating success
        return JsonResponse({'success': True})

    # Return a JSON response indicating failure
    return JsonResponse({'success': False})

def new_c_db(request):
   
    
    return render(request,'new_c_db.html')

def reg(request):
    return render(request,'reg.html')


def update_application_status(request):
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        application = AppliedJobs.objects.filter(id=application_id).select_related('job_id', 'user_id').first()
        
        # Check if the application exists
        if not application:
            return JsonResponse({'status': 'error', 'message': 'Application not found'}, status=404)
    
        user_email = application.user_id.email   
        smtp_server = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT
        sender_email = settings.EMAIL_HOST_USER
        sender_password = settings.EMAIL_HOST_PASSWORD

        # Prepare email content
        des = application.job_id.designation
        company_name = application.job_id.company_id.first_name
        
        subject = f'Congratulations!'
        body = f"""Dear {application.user_id.first_name},\nSending this mail to inform that you have been shortlisted for the profile {des} at {company_name}. You will be notified further soon"""
        
        try:
            # Send email
            send_mail(subject, body, sender_email, [user_email])
            
            # Update application status
            application.status = 'Selected'
            application.save()

            return JsonResponse({'status': 'success', 'message': 'Mail sent successfully'})
        except Exception as e:
            # Handle email sending failure
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def schedule_interview(request):
    if request.method == "POST":
        # Get form data
        user_id = request.POST.get("user_id")
        application = NewUser.objects.get(id=user_id)
        print(application.email)
        application_id = request.POST.get("application_id")
        designation = request.POST.get("designation")
        interview_date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        mode_of_interview = request.POST.get("mode_of_interview")
        
        try:
            # Prepare email content
            subject = 'Congratulations!'
            body = f"""Dear,\nSending this mail to inform that your interview have been scheduled for the profile {designation}  on {interview_date}\n
            Timing : {start_time} - {end_time}"""
            user_email = application.email   
            sender_email = settings.EMAIL_HOST_USER

            # Send email
            send_mail(subject, body, sender_email, [user_email])
            print("Mail sent successfully")
            
            # Save data to ScheduleInterview model
            schedule = ScheduleInterview.objects.create(
                user_id_id=user_id,
                application_id_id=application_id,
                interview_date=interview_date,
                start_time=start_time,
                end_time=end_time,
                mode_of_interview=mode_of_interview,  # Default value
                confirmation="Pending",  # Default value
                user_confirmation=False  # Default value
            )
            if schedule:
                print("Data stored successfully")

            return JsonResponse({'status': 'success'})
        except Exception as e:
            # Handle email sending failure
            print("Failed to send email:", str(e))
            return JsonResponse({'status': 'error', 'message': 'Failed to send email. Please check your network connection.'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
def saved_jobs(request):
    if request.user.user_type != 'job seeker':
        return HttpResponseForbidden()
    id = request.user.id
    obj = NewUser.objects.get(id=id)
    today_date = date.today()
    print("profileeee",obj.profile)
    # Fetch saved jobs from CompanyJobSaved model for the given user_id
    company_jobs = CompanyJobSaved.objects.select_related('companyIdOrAgencyId','job_id').filter(user_id=id)
    print("$$$$$$$$$$$",company_jobs)
    # Combine the job details from both models into a single variable
    all_saved_jobs = list(chain( company_jobs))
    print("////////////",all_saved_jobs)
    saved_company_jobs_ids = CompanyJobSaved.objects.filter(user_id=request.user.id).values_list('job_id_id', flat=True)
    print(saved_company_jobs_ids)
    saved_job_ids =  list(saved_company_jobs_ids)
    print("&&&&&&",saved_job_ids)
    for x in all_saved_jobs:
        print(x)
        days_since_posted = (timezone.now().date() - x.job_id.created_on).days
        x.days_since_posted = days_since_posted
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",x.days_since_posted)
        x.is_saved = x.job_id_id in saved_job_ids
        print("^^^^^^^^^^^^^",x.is_saved)
    # Merge the saved job IDs from both models
    saved_job_ids = list(saved_company_jobs_ids)
    unique_departments_job = JobDetails.objects.filter(J_type='job').values_list('department', flat=True).distinct()
    all_unique_departments = list(set(chain( unique_departments_job)))
    open_status_count_job = (
        JobDetails.objects.filter(status='open',J_type='job')
        .values('department')
        .annotate(open_count=Count('department'))
    )
    open_jobs_count = defaultdict(int)
    for item in open_status_count_job:
        open_jobs_count[item['department']] += item['open_count']
    department_open_counts = [
        (department, open_jobs_count.get(department, 0)) for department in all_unique_departments
    ]
    job_details_count = JobDetails.objects.filter(J_type='job').values('location').annotate(job_count=Count('location'))

# Count jobs in each unique location from AgencyJobDetails


# Combine the counts
    combined_counts = {}

    for job_detail in job_details_count:
        combined_counts[job_detail['location']] = combined_counts.get(job_detail['location'], 0) + job_detail['job_count']



    context = {'obj':obj,'today_date':today_date
    ,'department_open_counts':department_open_counts,'all_saved_jobs':all_saved_jobs,'combined_counts':combined_counts}
    return render(request,'saved_jobs.html',context)

def job_applications(request):
    if request.user.user_type != 'Company':
        return HttpResponseForbidden()
    
    success = request.GET.get('success', False)
    i = request.user.id
    first_name = request.user.first_name
    obj = NewUser.objects.get(id=i)
    today_date = date.today()

    # Fetch all distinct designations associated with job applications
    designations = AppliedJobs.objects.select_related('job_id').filter(job_id__company_id=i).values_list('job_id__designation', flat=True).distinct()

    # Get the selected designation filter from the GET request
    designation_filter = request.GET.get('designation', 'All')

    # Filter job applications based on the selected designation
    if designation_filter != 'All':
        data = AppliedJobs.objects.select_related('job_id', 'user_id').filter(job_id__company_id=i, job_id__designation=designation_filter)
    else:
        data = AppliedJobs.objects.select_related('job_id', 'user_id').filter(job_id__company_id=i)

    # Check if interview is scheduled for each application
    for item in data:
        item.interview_scheduled = ScheduleInterview.objects.filter(application_id=item.id).exists()

    context = {'obj': obj, 'data': data, 'first_name': first_name, 'success': success, 'designations': ['All'] + list(designations)}

    return render(request, 'job_applications.html', context)



@login_required
def application_status(request):
    if request.user.user_type != 'job seeker':
        return HttpResponseForbidden()
    id = request.user.id
    obj = NewUser.objects.get(id=id)
    today_date = date.today()
    applied_jobs = AppliedJobs.objects.select_related('job_id').filter(user_id_id=id)
    combined_jobs = list(applied_jobs)
    combined_jobs.sort(key=lambda x: x.applied_date, reverse=True)
    for x in combined_jobs:
        print(x)
    context = {'obj':obj,'today_date':today_date,'combined_jobs':combined_jobs}
    return render(request,'application_status.html',context)
@login_required
def companies(request):
    if request.user.user_type != 'job seeker':
        return HttpResponseForbidden()
    hiring_partners = NewUser.objects.filter(user_type='Company')
    context = {
    'hiring_partners':hiring_partners
    }
    return render(request,'companies.html',context)


def company_info(request,id):
    print("iddddddddd",id)
    obj = NewUser.objects.get(id=id)
    info = CompanyDetails.objects.filter(company_id_id=id).first()
    c_img = info.cover_image
    print(info.other_image1)
    print("LinkedIn URL:", info.linkedin_url)
    company_names = []
    company_jobs_dict = {}

    if obj.user_type == 'Company':
        # If the user is a company, retrieve jobs related to that company
        jobs = JobDetails.objects.filter(company_id_id=id,J_type='job')
        company_names = [obj.first_name]
        display_jobs = JobDetails.objects.filter(company_id_id=id,J_type='job')  # Assuming company_name exists in the NewUser model
        # Additional logic for companies if needed

    context = {
        'jobs': jobs,
        'company_names': company_names,
        'company_jobs_dict': company_jobs_dict,
        'obj': obj,
        'info':info,
        'c_img':c_img,
        'display_jobs':display_jobs

    }
    return render(request,'company_info.html',context)

from django.urls import reverse
def profile(request):
    success_message = request.GET.get('success_message')
    id = request.user.id
    obj = NewUser.objects.get(id=id)
    today_date = date.today()
    data = UserDetails.objects.filter(user_id=id).first()
   
    if request.method == 'POST':
        obj.first_name = request.POST.get('first_name')
        obj.last_name = request.POST.get('last_name')
        obj.email = request.POST.get('email')
        obj.city = request.POST.get('city')
        obj.linkedin = request.POST.get('linkedin')
        obj.country = request.POST.get('country')
        p = request.FILES.get('profile')
        data = UserDetails.objects.filter(user_id=id).first()  # Retrieve data again after POST
        
        if data is not None:
            data.qualification = request.POST.get('qualification')
            data.experience = request.POST.get('experience')
            data.skills = request.POST.get('skills')
            data.save()
        else:
            # Create a new UserDetails object if it doesn't exist
            data = UserDetails.objects.create(user_id_id=id, qualification=request.POST.get('qualification'), 
                                              experience=request.POST.get('experience'), 
                                              skills=request.POST.get('skills'))

        if p is not None:
            obj.profile = p

        obj.save()

    applied_jobs = AppliedJobs.objects.select_related('job_id').filter(user_id_id=id)
    combined_jobs = list(applied_jobs)
    combined_jobs.sort(key=lambda x: x.applied_date, reverse=True)
    no = len(combined_jobs)
    context = {'obj': obj, 'today_date': today_date, 'data': data, 'success_message': success_message, 'no': no}
    return render(request, 'profile.html', context)

def delete_application(request, pk):
    application = get_object_or_404(AppliedJobs, pk=pk)
    if request.method == 'POST':
        application.delete()
        # Redirect to the page where the table is displayed
        return redirect('job_applications')

def user_logout(request):
    logout(request)
    # Redirect to a specific page after logout (optional)
    return redirect('/')

def internships(request):

    data = JobDetails.objects.all().select_related('company_id').filter(status="open",J_type='internship')
    print(data)

    combined_data = list(chain(data))
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^",combined_data)
# Shuffle the combined list
    random.shuffle(combined_data)

    # Sort the combined list based on 'created_on' attribute to display recent jobs first
    combined_data.sort(key=lambda x: x.created_on, reverse=True)


# Display the jumbled results
    for item in combined_data:
        print(item)


    for x in combined_data:
        days_since_posted = (timezone.now().date() - x.created_on).days
        x.days_since_posted = days_since_posted

    context = {'data':data,'combined_data':combined_data,
    }
    return render(request,'internships.html',context)

def user_internship(request):

    data = JobDetails.objects.all().select_related('company_id').filter(status="open",J_type='internship')
    print(data)

    combined_data = list(chain(data))
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^",combined_data)
# Shuffle the combined list
    random.shuffle(combined_data)

    # Sort the combined list based on 'created_on' attribute to display recent jobs first
    combined_data.sort(key=lambda x: x.created_on, reverse=True)


# Display the jumbled results
    for item in combined_data:
        print(item)


    for x in combined_data:
        days_since_posted = (timezone.now().date() - x.created_on).days
        x.days_since_posted = days_since_posted

    context = {'data':data,'combined_data':combined_data,
    }
    return render(request,'user_internship.html',context)


def new_all_jobs(request):
    data = JobDetails.objects.all().select_related('company_id').filter(status="open",J_type='job')
    print(data)

    combined_data = list(chain(data))
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^",combined_data)
# Shuffle the combined list
    random.shuffle(combined_data)

    # Sort the combined list based on 'created_on' attribute to display recent jobs first
    combined_data.sort(key=lambda x: x.created_on, reverse=True)


# Display the jumbled results
    for item in combined_data:
        print(item)


    for x in combined_data:
        days_since_posted = (timezone.now().date() - x.created_on).days
        x.days_since_posted = days_since_posted



    unique_departments_job = JobDetails.objects.filter(J_type='job').values_list('department', flat=True).distinct()
    all_unique_departments = list(set(chain( unique_departments_job)))

    open_status_count_job = (
        JobDetails.objects.filter(status='open',J_type='job')
        .values('department')
        .annotate(open_count=Count('department'))
    )


    open_jobs_count = defaultdict(int)
    for item in open_status_count_job:
        open_jobs_count[item['department']] += item['open_count']



    department_open_counts = [
        (department, open_jobs_count.get(department, 0)) for department in all_unique_departments
    ]

    job_details_count = JobDetails.objects.filter(J_type='job').values('location').annotate(job_count=Count('location'))

# Count jobs in each unique location from AgencyJobDetails


# Combine the counts
    combined_counts = {}

    for job_detail in job_details_count:
        combined_counts[job_detail['location']] = combined_counts.get(job_detail['location'], 0) + job_detail['job_count']


    context = {'data':data,'combined_data':combined_data,
    'department_open_counts':department_open_counts,'combined_counts':combined_counts}
    return render(request,'new_all_jobs.html',context)


def new_user_register(request):
    return render(request,'new_user_register.html')

def temp4(request):
    return render(request,'temp4.html')


def pic(request):
    return render(request,'pic.html')

def A(request):
    return render(request,"A.html")

def calendar(request):
    id=request.user.id
    print(id)
    data=ScheduleInterview.objects.filter(user_id_id=id)
    context={'data':data}
    return render(request,"calendar.html" ,context)

def get_user_scheduled_interviews(request):
    user_id = request.user.id
    if request.method == 'GET' and 'date' in request.GET:
        date_str = request.GET.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d')
        date += timedelta(days=1)  # Add one day
        next_day_str = date.strftime('%Y-%m-%d')
        scheduled_interviews = ScheduleInterview.objects.select_related('user_id', 'application_id').filter(interview_date=next_day_str, user_id_id=user_id)

        interviews_list = []
        for interview in scheduled_interviews:
            interview_info = {
                'date': interview.interview_date,
                'start_time': interview.start_time,
                'end_time': interview.end_time,
                'mode_of_interview': interview.mode_of_interview,
                'designation': interview.application_id.job_id.designation,
                'company_name': interview.application_id.job_id.company_id.first_name
            }
            interviews_list.append(interview_info)

        return JsonResponse({'interviews': interviews_list})
    else:
        return JsonResponse({'error': 'Invalid request'})
