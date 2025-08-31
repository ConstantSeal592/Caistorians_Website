from django.urls import path, include
from . import views
from .views import create_product
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView

urlpatterns = [
    # Homepage showing products
    path('', views.product_list, name='product_list'),

    # User registration and authentication
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),  # Login/logout/password management

    # Profile URLs
    path('profile_detail/', views.my_profile, name='my_profile'),  # your own profile
    path('profile/edit_profile/', views.edit_profile, name='edit_profile'), # Edit profile
    path('profile/<str:username>/', views.profile, name='profile'),  # others' profiles

    # Public seller profile by username
    path('seller/<str:username>/', views.view_seller_profile, name='view_seller_profile'),

    # Manage own product listings
    path('manage-listings/', views.manage_listings, name='manage_listings'),
    path('product/<int:pk>/edit/', views.product_edit, name='product_edit'),

    # Product creation and details
    path('products/new/', views.create_product, name='create_product'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    path('products/<int:pk>/buy-now/', views.buy_now, name='buy_now'),
    path('confirmation', views.checkout_confirmation, name='checkout_confirmation'),

    # Basket views
    path('basket/', views.view_basket, name='view_basket'),
    path('basket/add/<int:pk>/', views.add_to_basket, name='add_to_basket'),
    path('basket/remove/<int:pk>/', views.remove_from_basket, name='remove_from_basket'),
    path('basket/update/', views.update_basket, name='update_basket'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # Checkout
    path('checkout', views.checkout, name='checkout'),

    # Personalized product list
    path('for-you/', views.personalized_product_list, name='for_you'),

    # Upload seller video
    path('upload-video/', views.upload_seller_video, name='upload_seller_video'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
