# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Message, Comment

def index(request):
    context = { 'users': User.objects.all() }
    return render(request, 'dashboard/index.html', context)

def addUser(request):
    if request.session['user_level'] == 9:
        if request.method == "GET":
            return render(request, 'dashboard/addUser.html')
        elif request.method == "POST":
            response_from_models = User.objects.addUser(request.POST)
            if response_from_models['status']:
                return redirect('db:index')
            else:
                for error in response_from_models['info']:
                    messages.add_message(request, messages.ERROR, error)
                return redirect('db:addUser')
    else:
        return render(request, 'dashboard/deny.html')

def edit(request, id):
    if request.session['user_level'] != 9 and request.session['user_id'] != int(id):
        return render(request, 'dashboard/deny.html')
    else:
        context = { 'user': User.objects.get(id=id) }
        return render(request, 'dashboard/profile.html', context)

def update(request, id):
    if request.method == "POST":
        postData = {'id': id}
        if request.POST['type'] == "info":
            postData['first_name'] = request.POST['first_name']
            postData['last_name'] = request.POST['last_name']
            postData['email'] = request.POST['email']
            try:
                postData['level'] = request.POST['level']
            except:
                pass
            fromModels = User.objects.updateInfo(postData)
            if fromModels['status']:
                messages.add_message(request, messages.INFO, "Changes saved.", extra_tags="personalinfo")
            else:
                for error in fromModels['info']:
                    messages.add_message(request, messages.ERROR, error, extra_tags="personalinfo")
        elif request.POST['type'] == "password":
            postData['password'] = request.POST['password']
            postData['confirm'] = request.POST['confirm']
            fromModels = User.objects.updatePassword(postData)
            if fromModels['status']:
                messages.add_message(request, messages.INFO, "Password updated.", extra_tags="password")
            else:
                for error in fromModels['info']:
                    messages.add_message(request, messages.ERROR, error, extra_tags="password")
        elif request.POST['type'] == "description":
            postData['description'] = request.POST['description']
            fromModels = User.objects.updateDescription(postData)
            if fromModels['status']:
                messages.add_message(request, messages.INFO, "Description updated.", extra_tags="desc")
            else:
                for error in fromModels['info']:
                    messages.add_message(request, messages.ERROR, error, extra_tags="desc")
        return redirect('db:edit', id=id)
    else:
        return redirect('db:index')

def show(request, id):
    context = { 'user': User.objects.get(id=id) }
    return render(request, 'dashboard/messages.html', context)

def addMessage(request, id):
    postData = { 'author_id': request.session['user_id'],
                 'recipient_id': id,
                 'message': request.POST['message'] }
    Message.objects.addMessage(postData)
    return redirect('db:show', id=id)

def addComment(request, id):
    postData = { 'author_id': request.session['user_id'],
                 'message_id': id,
                 'comment': request.POST['comment'] }
    comment = Comment.objects.addComment(postData)
    return redirect('db:show', id=comment.message.recipient.id)

def deleteUser(request, id):
    if request.session['user_level'] == 9:
        User.objects.get(id=id).delete()
        return redirect('db:index')
    else:
        return render(request, 'dashboard/deny.html')
