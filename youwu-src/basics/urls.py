"""site_youwu URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from site_youwu import views
import site_youwu.urls

urlpatterns = [

    url(r'^page=([0-9]{1,})/$', views.home_page),
    url(r'^site_youwu/', include(site_youwu.urls)),
    url(r'^', admin.site.urls),
    url(r'^albumId=([0-9]{1,})/pageId=([0-9]{1,})/$', views.album_page),
    url(r'^starId=([0-9]{1,})/pageId=([0-9]{1,})/$', views.star_page),
    url(r'^tagId=([0-9]{1,})/pageId=([0-9]{1,})/$', views.classify_page),
    url(r'^tag/pageId=([0-9]{1,})/$', views.classify_page),
]



