import json
import random

from django.conf import settings
from django.contrib import auth,messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import Courses, Registration, Opted_course, Temp_otp
from rest_framework import generics, viewsets, filters
from . import serializers
from .serializers import CourseSerializer
import datetime


# Create your views here.


def home(request):
    return render(request, 'appname/home.html')


def about(request):
    return render(request, 'appname/about.html')


def registration(request):
    if request.method == "POST":
        user = Registration()
        user.firstname = request.POST["firstname"]
        user.lastname = request.POST["lastname"]
        user.gender = request.POST["gender"]
        user.date = request.POST["date"]
        user.email = request.POST["email"]
        user.phonenumber = request.POST["phonenumber"]
        user.country = request.POST["country"]
        user.state = request.POST["state"]
        user.city = request.POST["city"]
        user.hobbies = json.dumps(request.POST["hobbies"])
        user.password = user.firstname + "@" + str(random.randint(1001, 9998))  # Generate a temporary password
        user.proflepicture = request.FILES["profilepicture"]
        if Registration.objects.filter(email=user.email).exists():
            messages.error(request, "existing email")
            print('existing email')
            return redirect('registration')
        else:
            password = user.password
            subject = "Hello welcome to my website"
            message = f'''<h1>Thankyou for registering to my website</h1><br> Temporary Password
                      Your temporary password is: {password}'''
            email_from = settings.EMAIL_HOST_USER
            recepient_email = [user.email]

            send_mail(subject, message, email_from, recepient_email,
                      html_message=message,
                      )
            request.session["pass"] = password
            user.save()
            return redirect('login')
    else:
        r_path = 'appname/registration.html'
        return render(request, r_path)


def contact_us(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        sub = request.POST["subject"]
        msg = request.POST["message"]
        subject1 = f"Hello {name}, welcome to Scope India"
        message1 = f'''<h1>Welcome to Scope India</h1><br> Thankyou so much for contacting us,
            We'll reach out to you as soon as possible.<br><br><br>Sincerely<br>Anu, customer service agent'''
        email_from = settings.EMAIL_HOST_USER
        recepient_email = [email]

        send_mail(subject1, message1, email_from, recepient_email,
                  html_message=message1,
                  )
        message_user = f"{sub},<br>{msg}<br> <br><br>from <br>{name},<br>{email}"
        send_mail("Enquiry", message_user, email_from, ["asmashirin000@gmail.com"],
                  html_message=message_user,
                  )
        return redirect('home')
    else:
        return render(request, 'appname/contact_us.html')


def courses(request):
    crs = Courses.objects.all()
    Course = [{"name": 'Software Programming Courses',
               "items":
                   [{
                       "id": 1,
                       "name": "JAVA FULL STACK INTERNSHIP"
                   },
                       {
                           "id": 2,
                           "name": "PYTHON FULL STACK INTERNSHIP"
                       },
                       {
                           "id": 3,
                           "name": "PHP FULL STACK INTERNSHIP"
                       },
                       {
                           "id": 4,
                           "name": ".NET CORE FULL STACK INTERNSHIP"
                       }, {
                       "id": 5,
                       "name": "MERN FULL STACK INTERNSHIP"
                   }, {
                       "id": 6,
                       "name": "MEAN FULL STACK INTERNSHIP"
                   }, {
                       "id": 7,
                       "name": "FLUTTER - ANDROID - iOS MOBILE APP INTERNSHIP"
                   }, {
                       "id": 8,
                       "name": "IONIC - ANDROID - iOS MOBILE APP INTERNSHIP"
                   }, {
                       "id": 9,
                       "name": "WEBSITE DESIGNING COURSE"
                   }]},
              {
                  "name": 'Software Testing Courses',
                  "items":
                      [{
                          "id": 1,
                          "name": "SOFTWARE TESTING ADVANCED INTERNSHIP"
                      }]},
              {
                  'name': 'Networking, Server & Cloud',
                  'items':
                      [{
                          "id": 1,
                          "name": "NETWORKING, SERVER AND CLOUD ADMINISTRATION"
                      }, {
                          "id": 2,
                          "name": "AWS ARCHITECT ASSOCIATE"
                      }, {
                          "id": 3,
                          "name": "MS AZUSE CLOUD ADMINISTRATOR"
                      }]},
              {
                  'name': 'Other Courses',
                  'items':
                      [{
                          "id": 1,
                          "name": "DIGITAL MARKETING COURSE AND INTERNSHIP"
                      }, {
                          "id": 2,
                          "name": "DATA SCIENCE"
                      }
                      ]}]
    return render(request, 'appname/courses.html', {'courses': Course})


def placement(request):
    return render(request, 'appname/placement.html')


def course_detail(request, name):
    crs = Courses.objects.filter(course_name=name)
    c = '',
    field = ''
    for item in crs:
        c = item.contents
        field = item.course_name
    c = c.split(",")
    print(c)
    return render(request, 'appname/course_detail.html', {'cors': c, "field": field})


def edit(request):
    if request.method == "POST":
        user_data = get_object_or_404(Registration, pk=request.session["user"][0]['userId'])
        user_data.firstname = request.POST["firstname"]
        user_data.lastname = request.POST["lastname"]
        user_data.email = request.POST["email"]
        user_data.phonenumber = request.POST["phonenumber"]
        user_data.address = request.POST["address"]
        user_data.proflepicture = request.FILES["profilepicture"]
        print(user_data.proflepicture)
        if Registration.objects.filter(email=user_data.email).exists():
            user_data.save()
            # User = Registration.objects.get(email=request.POST['email'])
            # Registration.objects.filter(pk=request.session["user"][0]['userId']).update(firstname=user.firstname,
            #                                                                             lastname=user.lastname,
            #                                                                             email=user.email,
            #                                                                             phonenumber=user.phonenumber,
            #                                                                             address=user.address,
            #                                                                             profilepicture=user.profilepicture,
            #                                                                             is_verified=True)
            # # user.save()
            return redirect("dashboard")
        else:
            print("user doesn't exists")
            return redirect('edit')
    else:
        User = Registration.objects.get(pk=request.session["user"][0]['userId'])
        return render(request, 'appname/edit.html', {"users": User})


def dashboard(request):
    user_details = Registration.objects.filter(pk=request.session["user"][0]['userId'])
    for user in user_details:
        course = Opted_course.objects.filter(userid=user.id)
    print(user_details)
    return render(request, 'appname/dashboard.html', {'details': user_details, 'o_course': course})


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            user = Registration()
            if Registration.objects.filter(email=request.POST['username']).exists():
                user = Registration.objects.get(email=request.POST['username'])
                if user.password == request.POST['password'] and user.is_verified == False:
                    request.session["user"] = [{
                        "userId": user.id,
                        "useremail": user.email
                    }]
                    return redirect('new_password')
                elif user.password == request.POST['password'] and user.is_verified == True:
                    request.session["user"] = [{
                        "userId": user.id,
                        "useremail": user.email
                    }]
                    return redirect("dashboard")
                else:
                    return redirect("login")
            else:
                messages.error(request, "Incorrect Username or Password")
                print("error")
                return redirect('login')
        else:
            return render(request, 'appname/login.html')


def logout(request):
    auth.logout(request)
    request.session['user_status'] = 'logged out'
    request.session['user_name'] = ''
    return redirect('login')


def forgot_password(request):
    if request.method == 'POST':
        user = Registration()
        if Registration.objects.filter(email=request.POST['email']).exists():
            user = Registration.objects.get(email=request.POST['email'])
            otp = random.randint(1001, 9998)  # Generate a temporary password
            temp = Temp_otp()
            temp.userid = user
            temp.otp = otp
            temp.save()
            subject = "Hello welcome to my website"
            message = f'''<h1>Temporary Password</h1><br> Temporary Password
                         Your temporary password is: {otp}'''
            email_from = settings.EMAIL_HOST_USER
            recepient_email = [user.email]

            send_mail(subject, message, email_from, recepient_email,
                      html_message=message,
                      )
            return redirect('otp')
        else:
            messages.error(request, "Invalid email")
            print("error")
            return redirect('login')
    else:
        return render(request, 'appname/forgot_password.html')


def code(request):
    if request.method == 'POST':
        temp = Temp_otp()
        temporary = request.POST["otp"]
        if Temp_otp.objects.filter(otp=temporary).exists():
            tempo = Temp_otp.objects.filter(otp=temporary)
            user = Registration()
            newpassword = request.POST['newpassword']
            Registration.objects.filter(pk=tempo[0].userid.id).update(password=newpassword)
            tempo.delete()
            return redirect('login')
        else:
            print("error")
            return redirect('otp')
    else:
        return render(request, 'appname/code.html')


def new_password(request):
    if request.method == 'POST':
        user = Registration()
        newpassword = request.POST['newpassword']
        Registration.objects.filter(pk=request.session["user"][0]['userId']).update(password=newpassword,
                                                                                    is_verified=True)
        return redirect('dashboard')
    else:
        return render(request, 'appname/new_password.html')


def enroll(request):
    if request.method == "POST":
        course_id = request.POST['course_id']
        user_id = request.session["user"][0]['userId']
        course_name = request.POST['course_name']
        course = Courses.objects.get(pk=course_id)
        user = Registration.objects.get(pk=user_id)
        optedcourse = Opted_course()
        optedcourse.courseid = course
        optedcourse.userid = user
        optedcourse.coursename = course_name
        date = datetime.datetime.now().strftime("%b %d,%Y %I:%M:%S %p")
        optedcourse.joindate = date
        optedcourse.save()
        return redirect('enroll')
    else:
        optedcourse = Opted_course.objects.all()
    return render(request, 'appname/enroll.html', {'optedcourse': optedcourse})


def delete(request):
    id = request.GET.get('id',None)
    dlt = Opted_course.objects.get(pk=id)
    dlt.delete()
    return redirect('enroll')


class Search(generics.ListCreateAPIView):
    # lookup_field = 'course_name'
    queryset = Courses.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['course_name']




