from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from shared.admin import BaseAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin, BaseAdmin):
    fieldsets = (*UserAdmin.fieldsets, ("", {"fields": ("can_import_export", "created", "modified")}))

    def has_import_permission(self, request):
        if getattr(request.user, "can_import", False):
            return True

        return super().has_import_permission(request)

    def has_export_permission(self, request):
        if getattr(request.user, "can_export", False):
            return True

        return super().has_export_permission(request)
