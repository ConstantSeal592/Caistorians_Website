from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.payment_form, name='payment_form'),
    path('success/', views.payment_success, name='payment_success'),
    path('history/', views.payment_history, name='payment_history'),
    path('refund-policy/', views.refund_policy, name='refund_policy'),
]
