from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
# from apps.users.models import *
import re
import bcrypt
import datetime
from django.utils import timezone


def index(request):
    context = {
        'number': User.objects.count(),
    }
    return render(request, 'login_app/index.html', context)


# def login_page(request):
#     return render(request, 'login_app/login.html')


# def registration_page(request):
#     return render(request, 'login_app/registration.html')


def registration(request):
    # if not valid_login(request):
    #     return redirect('/')
    if request.POST['form'] == 'register':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, key)
            return redirect('/')
        else:
            # live_user = User.objects.get(id=request.session['live_user'])
            # if live_user.user_level != 9:
            #     return redirect("/")
            if request.method == 'POST':
                password = request.POST['password']
                pw_hash = bcrypt.hashpw(
                    password.encode(), bcrypt.gensalt())  # create the hash
                print(pw_hash)
                # live_user = User.objects.create(
                #     first_name=request.POST['first_name'], user_level=1, last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
                # # if User.objects.count() == 1:
                # #     live_user.user_level = 9
                # if live_user.user_level == 9:
                #     request.session['live_user'] = live_user.id
                #     return redirect('/admin')
                # if live_user.user_level == 1:
                #     request.session['live_user'] = live_user.id
                #     return redirect("/users")
                # if User.objects.count >= 1:
                #     return redirect('/')
                # if User.objects.count() > 0:
                #     return redirect('/')
                live_user = User.objects.create(
                    first_name=request.POST['first_name'], user_level=1, last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash, delete='active')
                # live_user = User.objects.get(id=request.session['live_user'])
                # print('/* count'*10, User.objects.count())
                if User.objects.count() == 0:
                    live_user.user_level = 9
                if live_user.user_level == 9:
                    request.session['live_user'] = live_user.id
                    return redirect('/admin')
                # live_user = User.objects.get(id=request.session['live_user'])
                # if live_user.user_level == 9:
                #     request.session['live_user'] = live_user.id
                return redirect("/main")


def login(request):
    if request.POST['form'] == 'login':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, key)
            return redirect('/')
        else:
            user = User.objects.filter(email=request.POST['email'])
            if user:
                logged_user = user[0]
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    request.session['live_user'] = logged_user.id
                    # print('*'*10, logged_user.id, logged_user.user_level)
                    if logged_user.user_level == 12:
                        return redirect("/")
                    if logged_user.id == 1:
                        logged_user.user_level = 9

                    # print('*-'*10, logged_user.user_level)
                    if logged_user.user_level == 9:
                        return redirect('/admin')
                    if logged_user.user_level == 1:
                        return redirect('/main')
            messages.error(request, 'login Fail ')
    return redirect("/")


def logout(request):  # logout
    request.session.clear()
    return redirect('/')


def valid_login(request):
    if 'live_user' in request.session:
        return True
    return False
