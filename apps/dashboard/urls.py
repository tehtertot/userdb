from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^edit/(?P<id>\d*)$', views.edit, name="edit"),
    url(r'^update/(?P<id>\d*)$', views.update, name="update"),
    url(r'^messages/(?P<id>\d*)$', views.show, name="show"),
    url(r'^addUser$', views.addUser, name="addUser"),
    url(r'^addMessage/(?P<id>\d*)$', views.addMessage, name="addMessage"),
    url(r'^addComment/(?P<id>\d*)$', views.addComment, name="addComment"),
    url(r'^deleteUser/(?P<id>\d*)$', views.deleteUser, name="deleteUser")
]
