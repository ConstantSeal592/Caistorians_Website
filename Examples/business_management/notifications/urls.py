from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.notification_settings, name='notification_settings'),
    path('email-preview/', views.email_preview, name='email_preview'),]
