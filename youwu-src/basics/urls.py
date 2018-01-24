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
from django.views.generic.base import RedirectView
from django.contrib import admin
from site_youwu import views
import site_youwu.urls
import m_youwu.urls

urlpatterns = [
    url(r'^$', views.home_page),
    url(r'^index=([0-9]{1,})/$', views.home_page, name="home"),
    url(r'^site_youwu/', include(site_youwu.urls, namespace="site_youwu")),
    url(r'^m_youwu/', include(m_youwu.urls, namespace="m_youwu")),
    url(r'^albumId=([0-9]{1,})/pageId=([0-9]{1,})/$', views.album_page, name='album'),
    url(r'^starId=([0-9]{1,})/pageId=([0-9]{1,})/$', views.star_page, name='star'),
    url(r'^tagId=([a-zA-Z0-9]{1,})/pageId=([0-9]{1,})/$', views.classify_page, name='classify'),
    url(r'^tag/pageId=([0-9]{1,})/$', views.classify_page, name='classify_default'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    url(r'^fonts/glyphicons-halflings-regular\.woff2', RedirectView.as_view(url='/static/fonts/glyphicons-halflings-regular.woff2')),
    url(r'^fonts/glyphicons-halflings-regular\.woff', RedirectView.as_view(url='/static/fonts/glyphicons-halflings-regular.woff')),
    url(r'^fonts/glyphicons-halflings-regular\.ttf', RedirectView.as_view(url='/static/fonts/glyphicons-halflings-regular.ttf')),
    url(r'^fonts/glyphicons-halflings-regular\.svg', RedirectView.as_view(url='/static/fonts/glyphicons-halflings-regular.svg')),
    url(r'^admin', admin.site.urls),
]



