"""
URL configuration for business_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('salons/', include('salons.urls')),
    path('appointments/', include('appointments.urls')),
    path('scheduling/', include('scheduling.urls')),
    path('notifications/', include('notifications.urls')),
    path('payments/', include('payments.urls')),
    path('marketing/', include('marketing.urls')),
    path('analytics/', include('analytics.urls')),
    path('reviews/', include('reviews.urls')),
    path('settings/', include('settings_manager.urls')),
    path('integrations/', include('integrations.urls')),
]
