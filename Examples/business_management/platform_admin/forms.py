from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class ManagerCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'salon']

class ManagerEditForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'salon']
