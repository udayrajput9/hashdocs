from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(UserAdmin):
    model = Organization
    list_display = ['email', 'name', 'is_verified', 'date_joined', 'wallet_address']
    list_filter = ['is_verified', 'is_active', 'is_staff']
    search_fields = ['email', 'name']
    ordering = ['-date_joined']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Organization Info', {'fields': ('name', 'phone', 'website', 'address', 'logo', 'wallet_address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    readonly_fields = ['date_joined']
