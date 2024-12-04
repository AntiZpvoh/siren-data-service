from django.urls import path, include
from . import views
from django.urls import re_path as url

urlpatterns = [
    path('v1/session/', views.createSession),
    path('v1/session/<int:sessionId>/', views.getOrPutSession),
    path('v1/session/csv/<int:sessionId>/', views.getSessionQuestionsCSV),
    path('v1/question-group/', views.createQuestionGroup),
    path('v1/question/<int:questionGroupId>/', views.createQuestion),
]