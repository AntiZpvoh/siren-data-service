from django.urls import path, include
from . import views
from django.urls import re_path as url

urlpatterns = [
    path('upload_file/', views.upload_file),
    path('v1/session/', views.sessionAPI),
]