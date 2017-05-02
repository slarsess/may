# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
# regex formulas taken from my flask project, placed here for reference and quality control
# EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z0-9]*$")
# NAME_REGEX = re.compile(r"^[a-zA-z]{2,}$")
# PASSWORD_LENGTH = re.compile(r'^.{,8}$')
# PASSWORD_STRENGTH = re.compile(r'^(?=.*[A-Z])(?=.*[0-9])')
# NAME_REGEX = re.compile(r'[A-Za-z]')

# Create your models here.

# for validation and query
class UserManager(models.Manager):
    def validate_create(self,data):
        errors = []
        email_exists = User.objects.filter(email=data['email'])
        #lets validate first name, 2 letters min, cannot be blank
        if len(data['first_name']) < 2:
            errors.append("First name must be at least 2 letters")
        if not re.match(r'[A-Za-z]', data['first_name']):
            errors.append("First name must contain letters only--cannot be blank")
        #lets validate last name, 2 letter min, cannot be blank
        if len(data['last_name']) < 2:
            errors.append("Last name must be at least 2 letters")
        if not re.match(r'[A-Za-z]', data['last_name']):
            errors.append("Last name must contain letters only--cannot be blank")
        #lets validate email
        if not re.match(r"^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z0-9]*$", data['email']):
            errors.append('Invalid format for email')
        #validate password
        if not re.match(r'^.{,2}$', data['password']):
            errors.append("Your password must be at least 2***for testing**** characters")
        if data['password'] != data['confirm']:
            errors.append("Your passwords do not match")
        #lets see if this email exsists
        if len(email_exists) > 0:
            errors.append("Use a different email address")
        #encrypt password now that it matches
        if errors:
            return (False, errors)
        else:
            password = data['password']
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            #password is now hashed, lets enter the user into the db
            new_user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                password = hashed_pw,
            )
            return (True, new_user)

    def validate_login(self, data):
        errors = []
        email_exists = User.objects.filter(email=data['email'])
        if len(data['email']) < 1:
            errors.append('Email cannot be blank')
        if not re.match(r"^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z0-9]*$", data['email']):
            errors.append('Invalid format for email')
        if len(email_exists) == 0:
            errors.append('You must register first')
        if errors:
            return (False, errors)
        else:
            this_user = User.objects.get(email=data['email'])
            password = data['password']
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            if bcrypt.hashpw(password.encode(), this_user.password.encode()) == this_user.password.encode():
                print "password verified"
                return (True, this_user)
            else:
                errors.append("The password is incorrect")
                return (False, errors)



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
