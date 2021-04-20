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

"""Every element in the PATH refers to the specific object in views.py"""
urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('', views.login, name='login'),
    path('main', views.main_page, name='main'),
    path('log_ver', views.username_save, name='log_ver'),
    path('register', views.create_account, name='create_acc'),
    path('save_ver', views.account_safe, name='save_ver'),
    path('account/<str:username>', views.account_info, name='account'),
    path('my_channels', views.channel_views, name='my_channels'),
    path('create_video/<str:channel>/', views.video_create, name='create_video'),
    path('save_vid/<str:type>/<str:channel>', views.video_safe, name='save_vid'),
    path('video/<int:id>', views.video_page, name='video'),
    path('create_channel/', views.create_channel, name='create_channel'),
    path('channel_save', views.channel_safe, name='channel_safe'),
    path('comment_save/<str:username>/<int:video_id>/<int:id_replied>', views.comment_safe, name='comment_save'),
    path('channel/<str:channel>', views.channel_page, name='channel'),
    path('subscribe/<str:channel>', views.subscribe, name='subscribe'),
    path('unsubscribe/<str:channel>', views.unsubscribe, name="unsubscribe"),
    path('delete_channel/<str:channel>', views.channel_delete, name='delete_channel'),
    path('delete_video/<int:id>/<str:channel>', views.video_delete, name='delete_video'),
    path('search/', views.search, name='search'),
    path('history', views.history, name="history"),
    path('video_update/<int:id>', views.content_update, name='edit_content'),
    path('video_usafe/<int:id>', views.video_edit_safe, name='safe_edit'),
    path('start_stream/<int:id>', views.open_stream, name='start_stream'),
    path('delete_stream/<int:id>/<str:channel>', views.stream_delete, name='delete_stream'),
    path('stream/<int:id>', views.stream, name='stream'),
    path('create_stream/<str:channel>', views.create_stream, name="stream_create"),
    path('edit_stream/<int:id>', views.stream_update, name="edit_stream"),
    path('stream_usafe/<int:id>', views.stream_update_safe, name="stream_usafe"),
    path('stream_safe/<str:type>/<str:channel>', views.stream_safe, name="stream_safe"),
    path('account_update/', views.account_update, name="acccount_update"),
    path('acocunt_usafe/<str:acc>', views.account_usafe, name="account_usafe"),
    path('account_delete/<str:acc>', views.delete_acc, name="delete_acc")
]
