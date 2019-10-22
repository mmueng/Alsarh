from __future__ import unicode_literals
from django.db import models
from apps.login_app.models import User
from .models import *
import bcrypt
import re
from datetime import datetime
import datetime
from datetime import date


class CustomerManager(models.Manager):

    def Customer_validator(self, postData):

        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if(postData['first_name'] is None or postData['first_name'] is ''):
            errors["first_name"] = "First Name field is Required."
        elif len(postData['first_name']) < 2:
            errors["first_name"] = "First_name should be at least 2 characters"

        if(postData['last_name'] is None or postData['last_name'] is ''):
            errors["last_name"] = "Last Name field is Required."
        elif len(postData['last_name']) < 2:
            errors["last_name"] = "Last_name should be at least 2 characters"

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if(postData['email'] is None or postData['email'] is ''):
            errors["email"] = "E-mail field is Required."
        ########################################
        # # Unique Emaill Address
        if postData['email'] and Customer.objects.filter(email=postData['email']).exists():
            errors["email"] = "E-mail should be Unique ***************."
        ###########################################
        if len(postData['mobile']) < 11 or (postData['mobile']) == False:
            errors['mobile'] = 'Mobile number must contain at least 11 Number.'
        # ###############################
        # test whether a field matches the pattern

        if postData['country'] is None or postData['country'] is '':
            errors['country'] = 'Country field is required'
        elif len(postData['country']) < 2:
            errors["country"] = "Country should be at least 2 characters"
        if postData['city'] is None or postData['city'] is '':
            errors['city'] = 'city field is required'
        elif len(postData['city']) < 2:
            errors["city"] = "city should be at least 2 characters"
        if postData['city'] is None or postData['city'] is '':
            errors['city'] = 'city field is required'

        if postData['address1'] is None or postData['address1'] is '':
            errors['address1'] = 'Address field is required'
        return errors

    def Customer_edit_validator(self, postData):

        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if(postData['first_name'] is None or postData['first_name'] is ''):
            errors["first_name"] = "First Name field is Required."
        elif len(postData['first_name']) < 2:
            errors["first_name"] = "First_name should be at least 2 characters"

        if(postData['last_name'] is None or postData['last_name'] is ''):
            errors["last_name"] = "Last Name field is Required."
        elif len(postData['last_name']) < 2:
            errors["last_name"] = "Last_name should be at least 2 characters"

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if(postData['email'] is None or postData['email'] is ''):
            errors["email"] = "E-mail field is Required."
        ########################################
        # # Unique Emaill Address
        if postData['email'] and Customer.objects.filter(email=postData['email']).exists():
            errors["email"] = "E-mail should be Unique ***************."
        ###########################################
        if len(postData['mobile']) > 11 or (postData['mobile']) == False:
            errors['mobile'] = 'Mobile number must contain at least 11 Number.'
        # ###############################
        # test whether a field matches the pattern

        if postData['country'] is None or postData['country'] is '':
            errors['country'] = 'Country field is required'
        elif len(postData['country']) < 2:
            errors["country"] = "Country should be at least 2 characters"
        if postData['city'] is None or postData['city'] is '':
            errors['city'] = 'city field is required'
        elif len(postData['city']) < 2:
            errors["city"] = "city should be at least 2 characters"
        if postData['city'] is None or postData['city'] is '':
            errors['city'] = 'city field is required'

        if postData['address1'] is None or postData['address1'] is '':
            errors['address1'] = 'Address field is required'

        return errors

    def delete_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        # if(postData['deletemessage'] is None or postData['deletemessage'] is ''):
        errors["deletemessage"] = "You are not Authorized to delete this message."
        return errors


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name='created_customer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomerManager()


class Order(models.Model):
    user_to_order = models.ForeignKey(User, related_name='order_to_user')
    customer_order = models.ForeignKey(Customer, related_name='order_customer')
    design = models.CharField(max_length=255)
    design_type = models.CharField(max_length=255)
    requirment = models.CharField(max_length=255)
    delivery = models.DateField()
    status = models.CharField(max_length=255)
    deletes = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    joined_users = models.ManyToManyField(User, related_name="joined_order")


class History(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    deletes = models.CharField(max_length=255)
    completed = models.IntegerField()
    approved = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    orderHistory = models.ForeignKey(Order, related_name="HistoryOrder")
    userHistory = models.ForeignKey(User, related_name="HistoryUser")
