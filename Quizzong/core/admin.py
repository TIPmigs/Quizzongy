from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'name', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['is_active', 'is_staff']
    search_fields = ['email', 'username', 'github_username']
    ordering = ['username']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'name', 'github_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        # Removed 'Important Dates' section since 'date_joined' and 'last_login' are not editable
    )

    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'username', 'password1', 'password2')}),
        ('Personal Info', {'classes': ('wide',), 'fields': ('github_username',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
