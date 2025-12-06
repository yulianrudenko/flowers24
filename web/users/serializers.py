from django.core.exceptions import ValidationError
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "created_at",
        ]
        updatable_fields = ["first_name", "last_name", "phone"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data: dict):
        password = validated_data["password"]
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance: User, validated_data: dict):
        validated_data = {
            k: v for k, v in validated_data.items() if k in self.Meta.updatable_fields
        }

        return super().update(instance, validated_data)
