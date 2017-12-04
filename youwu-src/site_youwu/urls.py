from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^page=([0-9]{1,})/$', views.home_page),
    url(r'^albumID=([0-9]{1,})/$', views.album_page),
    url(r'^select/$', views.select),
]
