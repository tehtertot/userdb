# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User

def index(request):
    return render(request, 'login/index.html')

def login(request):
    if request.method == "GET":
        return render(request, 'login/login.html')
    elif request.method == "POST":
        response_from_models = User.objects.signUserIn(request.POST)
        if response_from_models['status']:
            setSessionVariables(request, response_from_models['info'])
            return redirect('db:index')
        else:
            for error in response_from_models['info']:
                messages.info(request, error)
            return redirect('login:login')

def register(request):
    if request.method == "GET":
        return render(request, 'login/register.html')
    elif request.method == "POST":
        response_from_models = User.objects.addUser(request.POST)
        if response_from_models['status']:
            setSessionVariables(request, response_from_models['info'])
            return redirect('db:index')
        else:
            for error in response_from_models['info']:
                messages.info(request, error)
            return redirect('login:register')

def logout(request):
    request.session.pop('username')
    request.session.pop('user_id')
    request.session.pop('user_level')
    return redirect('login:index')

def setSessionVariables(request, user):
    request.session['username'] = user.first_name
    request.session['user_id'] = user.id
    request.session['user_level'] = user.level
    print request.session['username']
    print request.session['user_id']
    print request.session['user_level']
