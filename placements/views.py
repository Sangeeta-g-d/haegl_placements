from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden,HttpResponseBadRequest
from django.template import loader
from .models import NewUser
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from datetime import datetime, timedelta
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
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
            return redirect('company_dashboard')
        else:
            request.session['error_message'] = 'Wait till account varifies'
            return redirect('/login')
    return render(request,'login.html')

def company_dashboard(request):
    return render(request,'company_dashboard.html')