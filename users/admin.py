from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "is_superuser",
        "is_staff",
        "is_active",
        "last_login",
        "date_joined",
    ]

    search_fields = ("email", "username", "first_name", "last_name")
    readonly_fields = ("date_joined", "last_login")

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide"),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            _("Personal Info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                )
            },
        ),
        (
            _("Permissions"),
            {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")},
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
