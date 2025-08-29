from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # avoids clash with auth.User.groups
        blank=True,
        help_text='The groups this user belongs to.'
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # avoids clash with auth.User.user_permissions
        blank=True,
        help_text='Specific permissions for this user.'
    )
