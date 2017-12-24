"""blog_mine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from app01 import views
from django_extra import xadmin
urlpatterns = [
    # url('admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^all/(?P<type_id>\d+)/', views.index),
    url(r'^login/', views.login),
    url(r'^signup/', views.signup),
    url(r'^check_code/', views.check_code),
    url(r'^updown.html$', views.updown),
    url(r'^(?P<site>\w+)/(?P<nid>\d+).html$', views.article),
    url(r'^(?P<site>\w+)/(?P<key>((tag)|(date)|(category)))/(?P<val>\w+-*\w*)/', views.filter),
    # url(r'^(\w+)/category/(\d+)/$', views.category),
    # url(r'^(\w+)/tag/(\d+)/$', views.tag),
    url(r'^(\w+)/$', views.home),
    # url(r'^(\w+)/(\d+)/$', views.home),
    url(r'^$', views.index),
]
