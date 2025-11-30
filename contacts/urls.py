from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.contacts, name='contacts'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('success/', views.contact_success, name='contact_success'),
]