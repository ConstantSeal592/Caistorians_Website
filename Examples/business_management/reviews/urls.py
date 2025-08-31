from django.urls import path
from . import views

urlpatterns = [
    path('<int:salon_id>/', views.review_list, name='review_list'),
    path('<int:salon_id>/new/', views.review_form, name='review_form'),
    path('moderate/', views.review_moderation, name='review_moderation'),
]
