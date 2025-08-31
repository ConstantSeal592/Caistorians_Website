from django.urls import path
from . import views

urlpatterns = [
    path('calendar/', views.staff_calendar, name='staff_calendar'),
    path('shift/new/', views.shift_form, name='shift_form'),
    path('leave/', views.leave_request, name='leave_request'),
    path('leave/history/', views.leave_list, name='leave_list'),
]
