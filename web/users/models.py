from uuid import uuid4

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser, PermissionsMixin):
    class UserManager(BaseUserManager):
        def create_user(self, password: str, **other_fields):
            other_fields.setdefault("is_staff", False)
            other_fields.setdefault("is_superuser", False)

            user = self.model(**other_fields)
            user.set_password(password)
            user.save()
            return user

        def create_superuser(self, password: str, **other_fields):
            other_fields.setdefault("is_staff", True)
            other_fields.setdefault("is_superuser", True)

            return self.create_user(password, **other_fields)

    USERNAME_FIELD = "email"

    objects = UserManager()

    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, db_index=True
    )
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(null=False, blank=False, validators=[MinLengthValidator(2)])
    last_name = models.CharField(null=False, blank=False, validators=[MinLengthValidator(2)])
    phone = PhoneNumberField(region="PL", unique=True)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    last_login = None

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.email}"
