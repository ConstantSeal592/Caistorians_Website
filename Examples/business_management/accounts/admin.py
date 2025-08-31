from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'salon')
    list_filter = ('role', 'salon')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'salon')}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Superusers see all users
        if request.user.is_superuser:
            return qs
        # Managers see only users in their salon
        if request.user.role == 'manager':
            return qs.filter(salon=request.user.salon)
        return qs.none()

    def save_model(self, request, obj, form, change):
        # When manager creates new user, force salon to be same as manager's
        if not request.user.is_superuser and request.user.role == 'manager':
            obj.salon = request.user.salon
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)

