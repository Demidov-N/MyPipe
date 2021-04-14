"""myPipeProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from myPipe import views

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('', views.login, name='login'),
    path('main', views.main_page, name='main'),
    path('log_ver', views.username_save, name='log_ver'),
    path('register', views.create_account, name='create_acc'),
    path('save_ver', views.account_safe, name='save_ver'),
    path('account/<str:username>', views.account_info, name='account'),
    path('my_channels', views.channel_views, name='my_channels'),
    path('create_video/<str:channel>/', views.video_create, name='create_video')
]
