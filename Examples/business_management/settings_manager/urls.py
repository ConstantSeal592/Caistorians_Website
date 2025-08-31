from django.urls import path
from . import views

urlpatterns = [
    path('general/', views.settings_form, name='settings_form'),
    path('hours/', views.working_hours_form, name='working_hours_form'),
    path('tax/', views.tax_settings, name='tax_settings'),
]
