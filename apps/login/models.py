# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re, bcrypt

email_regex = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')

class UserManager(models.Manager):
    def addUser(self, postData):
        #validations
        errors = []
        if not email_regex.match(postData['email']):
            errors.append("Invalid email address")
        try:
            User.objects.get(email=postData['email'])
            errors.append("A user with this password has already been registered")
        except:
            pass
        if len(postData['first_name']) < 1:
            errors.append("First name field is required")
        elif not postData['first_name'].isalpha():
            errors.append("First name should only contain letters")
        if len(postData['last_name']) < 1:
            errors.append("Last name field is required")
        elif not postData['last_name'].isalpha():
            errors.append("Last name should only contain letters")
        # if len(postData['password']) < 8:
        #     errors.append("Password should be at least 8 characters")
        if postData['password'] == "":
            errors.append("Password is required")
        if postData['password'] != postData['confirm']:
            errors.append("Passwords do not match")

        messages_to_views = {}
        if errors:
            messages_to_views['status'] = False
            messages_to_views['info'] = errors
        else:
            messages_to_views['status'] = True
            hashedpw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            if User.objects.all():
                messages_to_views['info'] = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], description="", password=hashedpw, level=1)
            else:
                messages_to_views['info'] = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], description="", password=hashedpw, level=9)
        return messages_to_views
    def signUserIn(request, postData):
        errors = []
        try:
            user = User.objects.get(email=postData['email'])
            if bcrypt.hashpw(postData['password'].encode(), user.password.encode()) != user.password.encode():
                errors.append("Wrong password. Try again.")
        except:
            errors.append("No user registered with that email")
        messages_to_views = {}
        if errors:
            messages_to_views['status'] = False
            messages_to_views['info'] = errors
        else:
            messages_to_views['status'] = True
            messages_to_views['info'] = user
        return messages_to_views
    def updateInfo(request, postData):
        user = User.objects.get(id=postData['id'])
        errors = []
        if postData['first_name'].isalpha() and len(postData['first_name']) > 1:
            user.first_name = postData['first_name']
        else:
            errors.append("Invalid first name")
        if postData['last_name'].isalpha() and len(postData['last_name']) > 1:
            user.last_name = postData['last_name']
        else:
            errors.append("Invalid last name")
        try:
            if user.email != postData['email']:
                User.objects.get(email=postData['email'])
                errors.append("This email is already associated with another user")
        except:
            if not email_regex.match(postData['email']):
                errors.append("Invalid email address")
            else:
                user.email = postData['email']
        if 'level' in postData:
            user.level = postData['level']

        messages_to_views = {}
        if errors:
            messages_to_views['status'] = False
            messages_to_views['info'] = errors
        else:
            user.save()
            messages_to_views['status'] = True
            messages_to_views['info'] = user
        return messages_to_views
    def updatePassword(request, postData):
        user = User.objects.get(id=postData['id'])
        errors = []
        if postData['password'] != postData['confirm']:
            errors.append("Passwords do not match")
        if postData['password'] == "":
            errors.append("Password cannot be empty")
        messages_to_views = {}
        if errors:
            messages_to_views['status'] = False
            messages_to_views['info'] = errors
        else:
            hashedpw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user.password = hashedpw
            user.save()
            messages_to_views['status'] = True
            messages_to_views['info'] = user
        return messages_to_views
    def updateDescription(request, postData):
        user = User.objects.get(id=postData['id'])
        errors = []
        if postData['description'] == user.description:
            errors.append("No changes made.")
        messages_to_views = {}
        if errors:
            messages_to_views['status'] = False
            messages_to_views['info'] = errors
        else:
            user.description = postData['description']
            user.save()
            messages_to_views['status'] = True
            messages_to_views['info'] = user
        return messages_to_views

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    level = models.PositiveSmallIntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    @property
    def user_level(self):
        if self.level == 9:
            return 'admin'
        else:
            return 'normal'
    def name(self):
        return self.first_name + " " + self.last_name
