from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'department', 'is_active')
    list_filter = ('role', 'is_active', 'department')
    fieldsets = UserAdmin.fieldsets + (
        ('Lab Info', {'fields': ('role', 'phone', 'department', 'bio', 'avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Lab Info', {'fields': ('role', 'phone', 'department')}),
    )
