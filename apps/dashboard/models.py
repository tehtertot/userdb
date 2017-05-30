# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login.models import User

class MessageManager(models.Manager):
    def addMessage(self, postData):
        auth = User.objects.get(id=postData['author_id'])
        rec = User.objects.get(id=postData['recipient_id'])
        Message.objects.create(message=postData['message'], recipient=rec, author=auth)

class CommentManager(models.Manager):
    def addComment(self, postData):
        auth = User.objects.get(id=postData['author_id'])
        message = Message.objects.get(id=postData['message_id'])
        return Comment.objects.create(comment=postData['comment'], message=message, author=auth)

class Message(models.Model):
    message = models.TextField()
    recipient = models.ForeignKey(User, related_name="messages_for")
    author = models.ForeignKey(User, related_name="messages_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class Comment(models.Model):
    comment = models.TextField()
    message = models.ForeignKey(Message, related_name="comments")
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()
