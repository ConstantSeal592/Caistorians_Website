from django.urls import path
from . import views

urlpatterns = [
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('campaigns/new/', views.campaign_form, name='campaign_form'),
    path('loyalty/', views.loyalty_dashboard, name='loyalty_dashboard'),
    path('promotions/new/', views.promotion_form, name='promotion_form'),
]
