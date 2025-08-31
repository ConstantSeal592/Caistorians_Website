from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.analytics_dashboard, name='analytics_dashboard'),
    path('staff/', views.staff_analytics, name='staff_analytics'),
    path('finance/', views.financial_report, name='financial_report'),
    path('services/', views.service_stats, name='service_stats'),]
