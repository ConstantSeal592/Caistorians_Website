from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("logout/", views.logout_view, name="logout"),
    path("billing/", views.billing_setup_view, name="billing_setup"),
    path("index/", views.index_view, name="index")
    
]
