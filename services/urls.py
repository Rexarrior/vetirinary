from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.services_list, name='list'),
    path('prices/', views.prices, name='prices'),
    path('<slug:slug>/', views.service_category, name='category'),
]

