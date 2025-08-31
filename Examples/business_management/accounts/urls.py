from django.urls import path
from . import views
from .views import create_manager_view

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('password/', views.password_change, name='password_change'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('create-staff/', views.create_staff_view, name='create_staff'),
    path('my-staff/', views.view_staff, name='my_staff'),
    path('create-manager/', create_manager_view, name='create_manager'),
    path('staff/<int:user_id>/delete/', views.staff_delete, name='staff_delete'),
    path('staff_dashboard/', views.staff_dashboard, name="staff_dashboard"),

]
