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
        extra_kwargs = {
            "password": {"write_only": True, "required": True}
        }

    def validate(self, attrs: dict):
        # Different config for POST and PATCH (create and partial update)
        if self.instance:
            field_names = [f.name for f in self.Meta.model._meta.get_fields()]
            instance_data = {
                k: getattr(self.instance, k)
                for k in field_names
                if hasattr(self.instance, k)
            }
            data = {**instance_data, **attrs}
            print(data)
        else:
            data = attrs

        try:
            User(**data).full_clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return attrs

    def create(self, validated_data: dict):
        password = validated_data["password"]
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance: User, validated_data: dict):
        # Password cannot be updated
        # TODO: separate endpoint?
        validated_data.pop("password")
        return super().update(instance, validated_data)
