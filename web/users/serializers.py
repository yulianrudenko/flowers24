from rest_framework import serializers

from users.models import User


class BaseUserSerializer(serializers.ModelSerializer):
    _hidden_from_others_fields = ["email", "phone"]

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
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
        }

    def create(self, validated_data: dict):
        password = validated_data["password"]
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserDetailSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        read_only_fields = BaseUserSerializer.Meta.read_only_fields + [
            "email",
        ]

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
