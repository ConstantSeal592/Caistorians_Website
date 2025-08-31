from django.urls import path
from . import views

urlpatterns = [
    path('xero/', views.xero_integration, name='xero_integration'),
    path('calendar/', views.calendar_sync_status, name='calendar_sync_status'),
    path('integration_settings/', views.integration_settings, name='integration_settings'),
]
