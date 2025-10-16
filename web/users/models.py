from uuid import uuid4

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):

    class UserManager(BaseUserManager):
        def create_superuser(
            self, email: str, password: str, **other_fields
        ):
            other_fields.setdefault("is_superuser", True)
            other_fields.setdefault("is_staff", True)
            if other_fields["is_superuser"] is not True:
                raise ValueError(_('Superuser"s "is_superuser" must be set to True'))
            user = self.model(email=email, **other_fields)
            user.set_password(password)
            user.save()
            return user

    USERNAME_FIELD = "email"

    objects = UserManager()

    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, db_index=True
    )
    email = models.EmailField(_("Email"), unique=True, null=False, blank=False)
    created_at = models.DateTimeField(_("Registration date"), auto_now_add=True)
    is_staff = models.BooleanField(_("Staff"), default=False)
    last_login = None

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.email}"
