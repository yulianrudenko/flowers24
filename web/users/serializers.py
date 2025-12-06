from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    _updatable_fields = ["first_name", "last_name", "phone"]
    _hidden_from_others_fields = ["email", "phone"]

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
        extra_kwargs = {
            "password": {"write_only": True},
            "created_at": {"read_only": True},
        }

    def create(self, validated_data: dict):
        password = validated_data["password"]
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance: User, validated_data: dict):
        validated_data = {
            k: v for k, v in validated_data.items() if k in self._updatable_fields
        }

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        request = self.context.get("request")
        if (
            request is not None
            and (request.user.is_staff or request.user.id == instance.id)
        ):
            return representation

        # Hide specific fields from other users
        for field in self._hidden_from_others_fields:
            representation.pop(field, None)

        return representation
