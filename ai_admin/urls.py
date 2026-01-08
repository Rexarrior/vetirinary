from django.urls import path
from . import views

app_name = 'ai_admin'

urlpatterns = [
    path('task/<int:task_id>/status/', views.task_status, name='task_status'),
    path('report/<slug:slug>/', views.view_report, name='view_report'),
]
