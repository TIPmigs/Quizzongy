from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff']
    search_fields = ['email', 'username']
    ordering = ['username']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'username', 'password1', 'password2')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)