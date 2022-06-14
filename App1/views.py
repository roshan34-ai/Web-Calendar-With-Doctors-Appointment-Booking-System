from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.template.loader import render_to_string, get_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, User, Appointment_User
from django.core.mail import EmailMultiAlternatives
from datetime import date, datetime, timedelta
from django.utils.html import strip_tags
from django.conf import settings


def index(request):
    if request.method=='POST':
        query=request.POST.get('search')
        if query is not None:
            specialist=CustomUser.objects.filter(profession__contains=query)
            return render(request, 'app1/home.html', {'specialists':specialist})
        
        name=request.POST.get('name')
        email=request.POST.get('email')
        question=request.POST.get('question')
        html_content = render_to_string('app1/askQuestion.html', {'name':name,
                                                                  'email':email,
                                                                  'question':question})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
                    "About Appointment Booking.",
                    text_content,
                    email,
                    [settings.EMAIL_HOST_USER],
                    )
        email.attach_alternative(html_content,"text/html")
        email.send()
    return render(request, 'app1/index.html')

def Home(request):
    if request.method=='POST':
        Query1=request.POST.get('filterByCity')
        Query2=request.POST.get('filterByLocality')
        Query3=request.POST.get('filterBySpeciality')
        specialist=CustomUser.objects.filter(dist_name__contains=Query1, locality__contains=Query2, profession__contains=Query3 )
        return render(request, 'app1/home.html', {'specialists':specialist})
    specialist=CustomUser.objects.all().order_by('specialist_name')
    return render(request, 'app1/home.html', {'specialists':specialist})

def Appointment(request):
    try:
        global instance
        global query_set
        global appointment

        specialist_id=request.POST.get('specialist')
        instance=CustomUser.objects.get(id=specialist_id) 
        query_set=CustomUser.objects.filter(id=specialist_id)
        appointment=User()  
        appointment.specialist_name=instance 
        
    except:
        if request.method=="POST":
            now = datetime.now()
            for x in range(8):
                d = now + timedelta(days=x)
            d=d.strftime("%Y-%m-%d")

            Date=request.POST.get('date')
            from_time=request.POST.get('time1')
            to_time=request.POST.get('time2')
            name=request.POST.get('name')
            email=request.POST.get('email')
            phone=request.POST.get('phone')
            appointment.date=Date
            appointment.from_time=from_time
            appointment.to_time=to_time 
            appointment.name=name
            appointment.email=email
            appointment.phone=phone
            if from_time <= d:
                appointment.save()
                html_content = render_to_string('app1/email.html', {'name':name,
                                                                    'date':Date,
                                                                    'time':from_time,
                                                                    'specialist':appointment.specialist_name.specialist_name,
                                                                    'phone':appointment.specialist_name.phone})
                text_content = strip_tags(html_content)
                email = EmailMultiAlternatives(
                            "About Your Appointment.",
                            text_content,
                            settings.EMAIL_HOST_USER,
                            [appointment.email],
                            )
                email.attach_alternative(html_content,"text/html")
                email.send() 
                return HttpResponseRedirect('home')
    
    days=[]
    time=[]
    t=None
    now = datetime.now()
    for x in range(7):
        d = now + timedelta(days=x)
        d=d.strftime("%Y-%m-%d")
        days.append(d)
    
    for day in days:
        Appt=User.objects.filter(specialist_name_id=specialist_id, date=day).order_by("date")
        for app in Appt:
            t=app
            time.append(t)
    time=time      
    return render(request, 'app1/book_appointment.html', {'Specialists' : query_set, "Days":days, "time":time})


def cancel_appointment(request, id):  
    user = User.objects.get(id=id)  
    user.delete() 
    html_content = render_to_string('app1/cancelBooking.html', {'name':user.name,
                                                        'date':user.date, 
                                                        'time':user.from_time,
                                                        'specialist':user.specialist_name.specialist_name, 
                                                        'phone':user.specialist_name.phone, 
                                                        'address':user.specialist_name.locality, 
                                                        'city':user.specialist_name.dist_name, 
                                                        'state':user.specialist_name.state_name, 
                                                        'pincode':user.specialist_name.pincode})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
               "About Your Appointment.",
               text_content,
               settings.EMAIL_HOST_USER,
               [appointment.email],
               )
    email.attach_alternative(html_content,"text/html")
    email.send()      
    return redirect("manage_appointment")  


def User_Registration(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        pwd=request.POST.get('password')
        password=make_password(pwd)
        user_obj=Appointment_User(
                   name=name,
                   email=email,
                   phone=phone,
                   password=password
                )
        user_obj.save()
        return HttpResponseRedirect('user_login')
    return render(request, 'app1/user_sign_up.html',)


def User_Login(request):
    if request.method == "POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=Appointment_User.get_appointment_user_by_email(email)
        if user:
            flag = check_password(password, user.password)
            if flag:
                request.session['email']=email
                request.session['name']=user.name
                return HttpResponseRedirect('home')
            else:
                return HttpResponseRedirect('user_login')
        else:
            return HttpResponseRedirect('user_login')
    return render(request, 'app1/user_log_in.html')


def logout(request):
    try:
        auth_logout(request)
        del request.session['email']
        del request.session['name']
    except:
        pass
    return redirect('index')


def register(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('number')
        image=request.FILES.get('image')
        address=request.POST.get('address')
        pincode=request.POST.get('pincode')
        city=request.POST.get('city')
        state=request.POST.get('state')
        qualification=request.POST.get('qualification')
        specialization=request.POST.get('specialization')
        experience=request.POST.get('experience')
        about=request.POST.get('about')
        fees=request.POST.get('fees')
        password=request.POST.get('password')
        confirmPassword=request.POST.get('confirmPassword')
        if password != confirmPassword:
            error_message="password missmatched!"
        password=make_password(password)
        user_obj=CustomUser(
                   specialist_name=name,
                   email=email,
                   phone=phone,
                   image=image,
                   password=password,
                   profession=specialization,
                   qualification=qualification,
                   locality=address,
                   state_name=state,
                   dist_name=city,
                   pincode=pincode,
                   experience=experience,
                   about=about,
                   cunsultation_fees=fees
        )
        user_obj.save()
        return HttpResponseRedirect('/login')
    return render(request, 'app1/doctor_sign_up_form.html',)


def login(request):
    if request.method == "POST":
        fm = AuthenticationForm(request = request, data = request.POST)
        if fm.is_valid():
            uemail = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(email = uemail, password = upass)
            if user is not None:
                auth_login(request, user)
                request.session['email']=uemail
                return HttpResponseRedirect("/home")
    else:
        fm = AuthenticationForm()
    return render(request, 'app1/doctor_login_page.html', {'form':fm})


def manage_appointment(request):
    if request.user.is_authenticated:
        data=User.objects.all()
        return render(request, 'app1/manage_appointment.html', {'Appointments':data})
    else:
        user=request.session.get('email')
        print(user)
        data=User.objects.filter(email=user)
        return render(request, 'app1/manage_appointment.html', {'Appointments':data})
    


def Contact(request):
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        question=request.POST.get('question')
        html_content = render_to_string('app1/askQuestion.html', {'name':name,
                                                                  'email':email,
                                                                  'question':question})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
                    "About Appointment Booking.",
                    text_content,
                    email,
                    [settings.EMAIL_HOST_USER],
                    )
        email.attach_alternative(html_content,"text/html")
        email.send()
    return render(request, 'app1/index.html')


def Profile(request, id):
    Consultant=CustomUser.objects.filter(id=id)
    return render(request, 'app1/doctor_profile_page.html', {'Consultants':Consultant})


def Profile_all(request):
    user=request.user.email
    Consultant=CustomUser.objects.filter(email=user)
    return render(request, 'app1/doctor_profile_page.html', {'Consultants':Consultant})


def reschedule_appointment(request, id):
    if request.method == "POST":
        date = request.POST.get('Date')
        print(date)
        from_time = request.POST.get('time1')
        print(from_time)
        to_time = request.POST.get('time2')
        print(to_time)
        user=User.objects.get(id=id)
        user.date=date
        user.from_time=from_time
        user.to_time=to_time
        user.save()
        html_content = render_to_string('app1/reScheduleBooking.html', {'name':user.name,
                                                                        'date':date, 
                                                                        'time':from_time, 
                                                                        'specialist':user.specialist_name.specialist_name, 
                                                                        'phone':user.specialist_name.phone, 
                                                                        'address':user.specialist_name.locality, 
                                                                        'city':user.specialist_name.dist_name, 
                                                                        'state':user.specialist_name.state_name, 
                                                                        'pincode':user.specialist_name.pincode})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
                   "About Your Appointment.",
                   text_content,
                   settings.EMAIL_HOST_USER,
                   [user.email],
                     #fail_silently = False
                   )
        email.attach_alternative(html_content,"text/html")
        email.send() 
        return redirect("manage_appointment")
    return render(request, 'app1/reSchedulingForm.html')


def User_reset_pass(request):
    try:
        if request.method=='POST':
            email=request.POST.get('email')
            new_pass=request.POST.get('newPassword')
            user=Appointment_User.objects.get(email=email)
            newPassword=make_password(new_pass)
            user.password=newPassword
            user.save()
            html_content = render_to_string('app1/newPassword.html', {'name':user.name,
                                                                     'new_pass':new_pass,})
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                       "About Your Appointment.",
                       text_content,
                       settings.EMAIL_HOST_USER,
                       [email],
                         #fail_silently = False
                       )
            email.attach_alternative(html_content,"text/html")
            email.send()
            return HttpResponseRedirect('user_login')
    except:
        pass     
    return render(request, 'app1/forgot_password.html')

def Doctor_reset_pass(request):
    try:
        if request.method=='POST':
            email=request.POST.get('email')
            new_pass=request.POST.get('newPassword')
            Doctor=CustomUser.objects.get(email=email)
            print(Doctor.specialist_name)
            newPassword=make_password(new_pass)
            Doctor.password=newPassword
            Doctor.save()
            html_content = render_to_string('app1/newPassword.html', {'name':Doctor.specialist_name,
                                                                      'new_pass':new_pass,})
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                        "About Your Appointment.",
                        text_content,
                        settings.EMAIL_HOST_USER,
                        [email],
                          #fail_silently = False
                        )
            email.attach_alternative(html_content,"text/html")
            email.send() 
            return HttpResponseRedirect('user_login')
    except:
        pass
    return render(request, 'app1/forgot_password.html')


