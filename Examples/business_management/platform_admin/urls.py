from django.urls import path
from . import views

urlpatterns = [
    path('create-manager/', views.create_manager_view, name='create_manager'),
    path('managers/', views.list_managers_view, name='list_managers'),
    path('edit-manager/<int:user_id>/', views.edit_manager_view, name='edit_manager'),
]