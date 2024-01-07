from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden,HttpResponseBadRequest
from django.template import loader
from .models import CompanyDetails, NewUser, JobDetails
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from datetime import datetime, timedelta
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.urls import reverse
# Create your views here.

def admin_db(request):
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

def company_logout(request):
    logout(request)
    # Redirect to a specific page after logout (optional)
    return redirect('/')

def registration(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_number')
        country = request.POST.get('country')
        state = request.POST.get('state')
        address = request.POST.get('address')
        city = request.POST.get('city')
        company_logo = request.FILES.get('profile')
        print("!!!!!!!!!",company_logo)
        about = request.POST.get('about')
        user_type = "Company"
        if password == password1:
            passw = make_password(password)
            user = NewUser.objects.create(first_name=company_name,username=username,password=passw,
            email=email,phone_no=contact_no,user_type=user_type, country=country,state=state,address=address,city=city,
            profile=company_logo,about=about)
            success_message = f"Registered successfully! Username: {username}, Password: {password}"
            request.session['success_message'] = success_message  # Store the success message in session

            return redirect('login')
        else:
            messages.error(request,'Password is not matching')

    return render(request,'registration.html')

def login1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        print(password)
        user = authenticate(request, username=username, password=password)
        print("!!!!!!!!!!!!!!!!",user)
        if user is not None and user.user_type == 'Company' and user.status == True:
            login(request, user)
            i = request.user.id
            print("companyyy idddd",i)
            record = CompanyDetails.objects.filter(company_id_id = i)
            if record:
                return redirect('/company_dashboard')
            else:
                return redirect('/company_details')
        else:
            request.session['error_message'] = 'Wait till account varifies'
            return redirect('/login')
        
    return render(request,'login.html')

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
          

def company_dashboard(request):
    first_name = request.user.first_name
    print(first_name)
    context = {
        'first_name':first_name
    }
    return render(request,'company_dashboard.html',context)


def job_vacancy(request):
    success_message = request.GET.get('success_message')
    i = request.user.id
    first_name = request.user.first_name
    obj = NewUser.objects.get(id=i)
    today_date = date.today()
    search_query = request.GET.get('search_query', '')

    data = JobDetails.objects.filter(company_id_id=i)

    if search_query:
        # Perform case-insensitive search for string fields
        data = data.filter(
            Q(designation__icontains=search_query) |
            Q(department__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(mandatory_skills__icontains=search_query) |
            Q(optional_skills__icontains=search_query) |
            Q(qualification__icontains=search_query) |
            Q(no_of_vacancy__icontains=search_query)
        )

        # Handle case-insensitive search for numeric fields by converting them to strings
        data = data.filter(
            Q(experience__icontains=str(search_query)) |
            Q(salary__icontains=str(search_query))
        )

    context = {'obj':obj,'today_date':today_date,'data':data,'success_message':success_message,'first_name':first_name}

    return render(request,'job_vacancy.html',context)

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
        description = request.POST.get('job_description')
        state = request.POST.get('state')
        country = request.POST.get('country')
        obj = JobDetails.objects.create(company_id_id=i,designation=designation,department=department,location=location,work_mode=work_mode,
        no_of_vacancy=no_of_vacancy,mandatory_skills=mandatory_skills,optional_skills=optional_skills,
        qualification=qualification,experience=experience,
        salary=salary,job_description=description)

        print(obj)
        return redirect(reverse('job_vacancy') + '?success_message=1')

    return render(request,'add_job.html',context)
