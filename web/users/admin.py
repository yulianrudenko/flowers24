from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["email", "is_superuser"]
    list_filter = ["is_superuser"]
    ordering = ["-created_at"]
    readonly_fields = [
        "id",
        "created_at",
    ]
    search_fields = ["id", "email"]

    fieldsets = [
        (None, {"fields": ["id", "email"]}),
        (_("Personal info"), {"fields": ["first_name", "last_name", "phone", "created_at"]}),
        (
            _("Permissions"),
            {
                "fields": [
                    "is_staff",
                    "is_superuser",
                ],
            },
        )
    ]
