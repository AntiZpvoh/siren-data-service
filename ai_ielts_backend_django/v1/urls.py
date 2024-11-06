from django.urls import path, include
from . import views
from django.urls import re_path as url

urlpatterns = [
    path('upload_file/', views.upload_file),
    path('v1/session/', views.createSession),
    path('v1/session/<int:sessionId>/', views.getSession),
    path('v1/session/csv/<int:sessionId>/', views.getSessionQuestionsCSV),
]