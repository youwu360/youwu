from django.conf.urls import url, include
from django.contrib import admin
from m_youwu import views

urlpatterns = [
    url(r'^index=([0-9]{1,})/$', views.home_page,name='m_home'),
    url(r'^albumId=([0-9]{1,})/pageId=([0-9]{1,})/$', views.album_page, name='m_album'),
    url(r'^starId=([0-9]{1,})/pageId=([0-9]{1,})/$', views.star_page, name='m_star'),
    url(r'^tagId=([0-9]{1,})/pageId=([0-9]{1,})/$', views.classify_page, name='m_classify'),
]
