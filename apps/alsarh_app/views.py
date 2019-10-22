from django.shortcuts import render, HttpResponse, redirect
from .models import *
from apps.login_app.models import User
from django.contrib import messages
import re
import bcrypt
import datetime
from django.utils import timezone


def index(request):
    if not valid_login(request):
        return redirect('/')
    context = {
        'live_user': User.objects.get(id=request.session['live_user']),
        'all_customers': Customer.objects.all(),
        'all_orders': Order.objects.all().order_by('delivery'),
        'all_users': User.objects.all(),
        'allhistory': History.objects.all(),
    }
    return render(request, 'alsarh_app/index.html', context)

def Historyst(request):
    if not valid_login(request):
        return redirect('/')
    context = {
        'live_user': User.objects.get(id=request.session['live_user']),
        'all_customers': Customer.objects.all(),
        'all_orders': Order.objects.all().order_by('delivery'),
        'all_users': User.objects.all(),
        'allhistory': History.objects.all(),
    }
    return render(request, 'alsarh_app/history.html', context)

def Join_order(request):
    if request.method == 'POST':
        # request the live user id
        live_user = request.session['live_user']
        live_user = User.objects.get(id=live_user)
        # request book that need to delete
        show = Order.objects.get(id=int(request.POST['order_id']))
        currUser = User.objects.get(id=request.POST['user_id'])
        print('*'*10, show, '-', currUser)
        # if live user = author who create the book then delete
        # if live_user != show.uploaded_by_id.id:
        currUserSelected = User.objects.get(id=request.POST['user'])
        show.status = 'Received'
        show.save()
        show.joined_users.remove(currUser)
        # show.joined_users.add(live_user)
        show.joined_users.add(currUserSelected)

        History.objects.create(orderHistory=show, userHistory=live_user,first_name=currUserSelected.first_name,last_name=currUserSelected.last_name,status=show.status, deletes = show.deletes,completed = 0, approved =0)
    return redirect('/main')


def assign_order_to(request):
        # request the live user id
        live_user = request.session['live_user']
        live_user = User.objects.get(id=live_user)
        # request book that need to delete
        show = Order.objects.get(id=int(request.POST['order_id']))
        currUser = User.objects.get(id=request.POST['user'])
        print('*'*10, show, '-', currUser)
        # if live user = author who create the book then delete
        # if live_user != show.uploaded_by_id.id:
        show.status = 'Received'
        show.save()
        show.joined_users.remove(live_user)
        show.joined_users.add(currUser)
        # orders = Order.objects.get(id=int(orderID))
        # user = User.objects.get(id=request.session['live_user'])
        History.objects.create(orderHistory=show, userHistory=live_user,first_name=currUser.first_name,last_name=currUser.last_name,status=show.status, deletes = show.deletes, approved=0,completed=0)
        return redirect('/main')

def new(request):
    if not valid_login(request):
        return redirect('/')
    live_user = request.session['live_user']
    live_user = User.objects.get(id=live_user)
    context = {
        'live_user': User.objects.get(id=request.session['live_user']),
    }
    return render(request, 'alsarh_app/new.html',context)


def add_customer(request):
    if not valid_login(request):
        return redirect('/')
    errors = Customer.objects.Customer_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, key)
        return redirect('/main/new')
    else:
        user = User.objects.get(id=request.session['live_user'])
        new = Customer.objects.create(
            first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], mobile=request.POST['mobile'], country=request.POST['country'], city=request.POST['city'], address1=request.POST['address1'], address2=request.POST['address2'], creator=user)
        new = Customer.objects.get(id=new.id)
        print('_'*10, new.id, '*'*10)
        # return redirect('/main')
        return redirect(f'/main/neworder/{new.id}/show')

# def edit(request):
#     if not valid_login(request):
#         return redirect('/')
#     return render


def edit(request, customerID):
    context = {
        'customer': Customer.objects.get(id=customerID),
    }
    return render(request, 'alsarh_app/edit.html', context)


def edit_customer(request, customerID):
    if not valid_login(request):
        return redirect('/')
    # # errors = Customer.objects.Books_validator(request.POST)
    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value, key)
    #     return redirect('/book/'+bookID)
    # else:
    if request.method == 'POST':
            # request the live user id
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        country = request.POST['country']
        city = request.POST['city']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        live_user = request.session['live_user']
        live_user = User.objects.get(id=live_user)
        # request book that need to delete

        show = Customer.objects.get(id=customerID)
        # print('*'*10, live_user, '*'*3, show.uploaded_by_id.id)
        # if live user = author who create the book then delete
        # if live_user in show.book_to_user.all():
        show.first_name = first_name
        show.last_name = last_name
        show.email = email
        show.country = country
        show.city = city
        show.address1 = address1
        show.address2 = address2
        show.save()
        return redirect(f'/main/neworder/{customerID}/show')


def new_order(request):
    if not valid_login(request):
        return redirect('/')
    context = {
        'live_user': User.objects.get(id=request.session['live_user']),
        'all_customers': Customer.objects.all(),
    }
    return render(request, 'alsarh_app/neworder.html', context)


def show(request, customerID):
    if not valid_login:
        return redirect('/')
    print('*'*10, customerID)
    context = {
        'live_user': User.objects.get(id=request.session['live_user']),
        'customer': Customer.objects.get(id=customerID),
        'all_customers': Customer.objects.all(),
        'all_users': User.objects.all(),
        'allhistory': History.objects.all(),
    }
    return render(request, 'alsarh_app/show.html', context)


def add_order(request, customerID):
    if not valid_login(request):
        return redirect('/')
    # errors = Customer.objects.Customer_validator(request.POST)
    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value, key)
    #     return redirect('/main/new')
    # else:
    user = User.objects.get(id=request.session['live_user'])
    customer = Customer.objects.get(id=customerID)
    # staff = User.objects.get(id=request.POST['engineer'])
    print(customer)
    Order.objects.create(
        design=request.POST['design'], design_type=request.POST['design_type'], requirment=request.POST['requirment'],
        delivery=request.POST['delivery'],deletes = 'add',status='Received', customer_order=customer, user_to_order=user).joined_users.add(int(request.POST['engineer']))
    
    # print("*"*10, creOrder)
    # currOrder = Order.objects.get(id = creOrder)
    # print("*"*10, currOrder)
    # History.objects.create(orderHistory = creOrder.id)

    return redirect('/main')


def edit_order(request, customerID, orderID):
    context = {
        'customer': Customer.objects.get(id=customerID),
        'order': Order.objects.get(id=orderID),
        'all_users': User.objects.all(),
    }
    return render(request, 'alsarh_app/editorder.html', context)


def edit_order_process(request, customerID, orderID):
    if not valid_login(request):
        return redirect('/')
    # # errors = Customer.objects.Books_validator(request.POST)
    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value, key)
    #     return redirect('/book/'+bookID)
    # else:
    if request.method == 'POST':
            # request the live user id
        engineer = request.POST['engineer']
        design = request.POST['design']
        design_type = request.POST['design_type']
        delivery = request.POST['delivery']
        requirment = request.POST['requirment']

        # live_user = User.objects.get(id=live_user)
        # request book that need to delete

        # customer = Customer.objects.get(id=customerID)
        show = Order.objects.get(id=orderID)
        # print('*'*10, live_user, '*'*3, show.uploaded_by_id.id)
        # if live user = author who create the book then delete
        # if live_user in show.book_to_user.all():
        show.engineer = engineer
        show.design = design
        show.design_type = design_type
        show.delivery = delivery
        show.requirment = requirment
        show.save()
        orders = Order.objects.get(id=int(orderID))
        user = User.objects.get(id=request.session['live_user'])
        History.objects.create(orderHistory=orders, userHistory=user,first_name=user.first_name,last_name=user.last_name,status=orders.status, deletes = orders.deletes,approved = 0,completed=0)
    return redirect(f'/main/neworder/{customerID}/{orderID}/show')


def show_order(request, customerID, orderID):
    if not valid_login:
        return redirect('/')
    # print('*'*10, customerID)

    context = {
        'live_user': User.objects.get(id=request.session['live_user']),
        'customer': Customer.objects.get(id=customerID),
        'order': Order.objects.get(id=orderID),
        'all_customers': Customer.objects.all(),
        'all_users': User.objects.all(),
        'allhistory': History.objects.all().order_by('-created_at'),
        'all_comments': Comments.objects.all(),

    }
    return render(request, 'alsarh_app/order.html', context)


def status(request,customerID, orderID):
    if not valid_login:
        return redirect('/')
    user = User.objects.get(id=request.session['live_user'])

    print('='*10,request.session['live_user'])
    orders = Order.objects.get(id=int(orderID))
    print('*'*10,orders.id)
    orders.status = request.POST['status']
    if request.POST['status'] == 'Compleated':
        completed = 1
    else:
        completed = 0
    if request.POST['status'] == 'Approved':
        approved = 1
    else:
        approved = 0
    History.objects.create(orderHistory=orders, userHistory=user,first_name=user.first_name,last_name=user.last_name,status=request.POST['status'], deletes = orders.deletes,approved =approved,completed= completed)
    orders.save()
    return redirect(f'/main/neworder/{customerID}/{orderID}/show')

def post_comment(request,customerID, orderID):
    if not valid_login(request):
        return redirect('/')
    user = User.objects.get(id=request.session['live_user'])
    orders = Order.objects.get(id=int(orderID))
    # message = request.message
    print('****'*20, user.id, '****'*20)
    request.POST['comment']
    if request.POST['comment'] is '':
        return redirect(f'/main/neworder/{customerID}/{orderID}/show')
    Comments.objects.create(
        comment=request.POST['comment'], user_to_comment=user, message_to_comment=orders)
    messages.success(request, "Post a Message successfully Created")
    return redirect(f'/main/neworder/{customerID}/{orderID}/show')

def remove(request, orderID):
    if not valid_login:
        return redirect('/')
    orders = Order.objects.get(id=int(orderID))
    print('*'*10,orders.id)
    orders.deletes = str('delete')
    user = User.objects.get(id=request.session['live_user'])
    # orders = Order.objects.get(id=int(orderID))
    orders.save()
    print(user.first_name, " - ", orders.status, " - ",orders.deletes, "*"*10)
    History.objects.create(orderHistory=orders, userHistory=user,first_name=user.first_name,last_name=user.last_name,status=orders.status, deletes = orders.deletes, completed=0,approved=0)
    return redirect('/main')


def remove2(request,customerID, orderID):
    if not valid_login:
        return redirect('/')
    orders = Order.objects.get(id=int(orderID))
    print('*'*10,orders.id)
    orders.deletes = str('delete')
    orders.save()

    user = User.objects.get(id=request.session['live_user'])
    History.objects.create(orderHistory=orders, userHistory=user,first_name=user.first_name,last_name=user.last_name,status=orders.status, deletes = orders.deletes,completed=0,approved=0)
    return redirect('/main')

def return_to_tasks(request, orderID):
    if not valid_login:
        return redirect('/')
    orders = Order.objects.get(id=int(orderID))
    print('*'*10,orders.id)
    orders.deletes = str('add')
    orders.save()
    user = User.objects.get(id=request.session['live_user'])
    History.objects.create(orderHistory=orders, userHistory=user,first_name=user.first_name,last_name=user.last_name,status=orders.status, deletes = orders.deletes,completed=0,approved=0)
    return redirect('/admin')

def delete(request, orderID):
    if not valid_login:
        return redirect('/')
    orders = Order.objects.get(id=int(orderID))
    user = User.objects.get(id=request.session['live_user'])
    History.objects.create(orderHistory=orders, userHistory=user,first_name=user.first_name,last_name=user.last_name,status=orders.status, deletes = orders.deletes,completed=0,approved=0)
    print('*'*10,orders.id)
    orders.delete()
    return redirect('/admin')


def valid_login(request):
    if 'live_user' in request.session:
        return True
    return False
