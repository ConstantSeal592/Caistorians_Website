from django.urls import path
from . import views
from .views import *
app_name = 'salons'

urlpatterns = [
    path('', views.salon_list, name='salon_list'),
    path('<int:pk>/', views.salon_detail, name='salon_detail'),
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/<int:id>/', views.staff_detail, name='staff_detail'),
    path('create/', views.salon_create, name='salon_create'),
    path('salon_edit/<int:salon_id>/', views.salon_edit, name='edit_salon'),
    path('assign-salon/<int:user_id>/', assign_salon_view, name='assign_salon'),
    path('<int:pk>/services/', views.service_list, name='service_list'),
    path('services/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('<int:salon_id>/services/new/', views.service_form, name='service_form'),
    path('salon_delete/<int:salon_id>/', views.salon_delete, name='salon_delete'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),
    path('edit_opening_hours', views.service_delete, name='service_delete'),
    path('opening-hours/edit/', edit_opening_hours, name='edit_opening_hours'),
    path('holidays/add/', views.holiday_create_view, name='holiday_add'),
    path('holidays/<int:holiday_id>/edit/', views.holiday_edit_view, name='holiday_edit'),
    path('holidays/<int:holiday_id>/delete/', views.holiday_delete_view, name='holiday_delete'),
    path('opening-hours/', views.opening_hours_list, name='opening_hours_list'),
    path('holidays/', views.holiday_list_view, name='holiday_list'),
    path('staff/shifts/', views.manage_shifts, name='manage_shifts'),
    path('skip_shift/<int:shift_id>/<str:date_str>/', views.skip_shift, name='skip_shift'),


]
