# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from models import User
# Create your views here.

def index(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'logapp/index.html', context)

def register(request):
    if request.method == 'POST':
        valid, data = User.objects.validate_create(request.POST)
        if valid == True:
            print "Registration was successful"
        else:
            for error in data:
                messages.error(request,error)
            return redirect('/')
    context = {
        'users': User.objects.all(),
    }
    current_user = User.objects.validate_create(request.POST)
    request.session['first_name'] = request.POST['first_name']
    return redirect ('belt:index')

def login(request):
    if request.method == 'POST':
        valid, data = User.objects.validate_login(request.POST)
        if valid == True:
            print "successful login"
        else:
            for error in data:
                messages.error(request, error)
            return redirect('/')
    context = {
        "users": User.objects.all()
    }
    current_user = User.objects.validate_login(request.POST)
    request.session['id'] = current_user[1].id
    request.session['first_name'] = current_user[1].first_name
    return redirect ('belt:index')

def logout(request):
    request.session.clear()
    return redirect('/')
