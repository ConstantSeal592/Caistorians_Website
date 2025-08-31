from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('staff', 'Staff'),
        ('manager', 'Manager'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    salon = models.ForeignKey(
        'salons.Salon',  # Use string reference here to avoid circular import
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='users'
    )

    def clean(self):
        if self.role == 'staff' and self.salon is None:
            raise ValidationError("Staff must be assigned to a salon.")
        if self.role == 'client' and self.salon is not None:
            raise ValidationError("Clients cannot be assigned to a salon.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

