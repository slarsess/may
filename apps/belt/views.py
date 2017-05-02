# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import F
from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from ..logapp.models import User
# from models import Review
from django.contrib import messages


# Create your views here.
def index(request):
    if 'id' not in request.session:
        messages.error(request, "You must be logged in first.")
        return redirect('logapp:index')
    return render(request, "belt/index.html", context)
