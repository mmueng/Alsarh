from django.shortcuts import render, HttpResponse, redirect
from apps.login_app.models import User
from .models import *
from .models import *
from apps.alsarh_app.models import Customer, Order
from django.contrib import messages
import re
import bcrypt
import datetime
from django.utils import timezone


def index(request):
    if not valid_login(request):
        return redirect('/')
    # if not admin user not allowed to add users
    live_user = User.objects.get(id=request.session['live_user'])
    if live_user.user_level != 9:
        return redirect('/')
    if live_user.id == 1:
        live_user.user_level = 9
    ###################################
    live_user = request.session['live_user']
    user_admin = User.objects.get(id=1)
    user_admin.user_level = 9
    context = {
        'live_user': User.objects.get(id=live_user),
        'all_users': User.objects.all(),
        'user_admin': user_admin,
        'all_orders': Order.objects.all(),
    }
    return render(request, 'admin_app/index.html', context)


def new(request):
    if not valid_login(request):
        return redirect('/')
    # if not admin user not allowed to add users
    live_user = User.objects.get(id=request.session['live_user'])
    if live_user.user_level != 9:
        return redirect('/')
    ########################################
    context = {
        'live_user': User.objects.get(id=request.session['live_user']).first_name
    }
    return render(request, 'admin_app/new.html', context)


def edit(request, userID):
    if not valid_login(request):
        return redirect('/')

    live_user = request.session['live_user']
    # if not admin user not allowed to add users
    live_user = User.objects.get(id=request.session['live_user'])
    if live_user.user_level != 9:
        return redirect('/')
    ################################

    context = {
        'edit': User.objects.get(id=int(userID)),
        'live_user': live_user,
    }
    return render(request, 'admin_app/edit.html', context)


def process_edit(request, userID):
    if not valid_login(request):
        return redirect('/')
    # if not admin user not allowed to add users
    live_user = User.objects.get(id=request.session['live_user'])
    if live_user.user_level != 9:
        return redirect('/')
    errors = User.objects.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, key)
        return redirect(f'/admin/{userID}/edit')
    else:
        live_user = request.session['live_user']
        current = User.objects.get(id=live_user)
        print('*c'*20, current.user_level)

        user = User.objects.get(id=userID)
        print('*'*20, user, live_user)
        if current.user_level == 9:
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
        # user.email = request.POST['email']
        # user.password = request.POST['password']
            user.user_level = request.POST['user_level']
            print('*'*10, user.first_name, '-',
                  user.last_name, user.user_level)
            user.save()
        return redirect('/admin')


def delete(request, userID):
    if not valid_login(request):
        return redirect('/')
    # if request.method == 'POST':
        # request the live user id
    live_user = request.session['live_user']
    # request user that need to delete
    user = User.objects.get(id=userID)
    user.delete = 'Delete'
    user.user_level = 12
    user.save()
    # if live user = author who create the book then delete
    # user.delete()
    return redirect('/admin')


def valid_login(request):
    if 'live_user' in request.session:
        return True
    return False
