from django.contrib import admin
from users.models import TenantUser

from tenant_users.permissions.models import UserTenantPermissions


@admin.register(TenantUser)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "name",
    )
    search_fields = (
        "email",
        "name",
    )


@admin.register(UserTenantPermissions)
class UserTenantPermissionsAdmin(admin.ModelAdmin):
    list_display = ("profile",)
    autocomplete_fields = ("profile",)
