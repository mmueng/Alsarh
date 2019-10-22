from __future__ import unicode_literals
from django.db import models
# from apps.users.models import *
# from apps.admin_app.models import *
import bcrypt
import re
from datetime import datetime
import datetime
from datetime import date


class UserManager(models.Manager):

    def basic_validator(self, postData):

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
        if postData['email'] and User.objects.filter(email=postData['email']).exists():
            errors["email"] = "E-mail should be Unique ***************."
        ###########################################

        # ###############################
        # test whether a field matches the pattern

        if postData['password'] is None or postData['password'] is '':
            errors['password'] = 'password field is required'
        elif len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['confirm'] != postData['password']:  # check for pw match
            errors['confirm'] = 'confirmation - passwords do not match'
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # test whether a field matches the pattern

        if(postData['email'] is None or postData['email'] is ''):
            errors['email_log'] = "E-mail field is Required."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_log'] = ("Invalid email address!")

        if postData['password'] is None or postData['password'] is '':
            errors['password_log'] = 'password field is required'
        elif len(postData['password']) < 8:
            errors["password_log"] = "Password should be at least 8 characters"

        userList = User.objects.filter(email=postData['email'])

        if (len(userList) < 1):
            errors['email_log'] = 'No account matches this email address.'
        elif (len(userList) == 1):
            curUser = userList[0]
            if not bcrypt.checkpw(postData['password'].encode(), curUser.password.encode()):
                errors['password_log'] = 'Wrong e-mail or password.'
        return errors

    def edit_validator(self, postData):

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

        ###########################################

        # ###############################
        # test whether a field matches the pattern

        if postData['user_level'] is None or postData['user_level'] is '' or postData['user_level'] == 0:
            errors['user_level'] = 'user_level field is required'
        return errors

    def delete_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        # if(postData['deletemessage'] is None or postData['deletemessage'] is ''):
        errors["deletemessage"] = "You are not Authorized to delete this message."

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    delete = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_level = models.IntegerField()
    objects = UserManager()
