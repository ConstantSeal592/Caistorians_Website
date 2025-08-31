from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.booking_form, name='booking_form'),
    path('confirm/', views.booking_confirm, name='booking_confirm'),
    path('success/', views.booking_success, name='booking_success'),
    path('my/', views.my_appointments, name='my_appointments'),
    path('<int:id>/', views.appointment_detail, name='appointment_detail'),
    path('queue/', views.queue_status, name='queue_status'),
]
