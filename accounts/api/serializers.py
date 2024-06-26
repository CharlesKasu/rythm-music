from rest_framework import serializers

from ..models import *


class UserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs["partial"] = True
        super(UserSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        # fields = "__all__"
        exclude = (
            "password",
            "user_permissions",
            "groups",
            "is_staff",
            "is_active",
            "is_superuser",
            "last_login",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True, label="Confirm password")

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password2",
            "name",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        name = validated_data["name"]
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Email addresses must be unique."})
        if password != password2:
            raise serializers.ValidationError({"password": "The two passwords differ."})
        user = User(email=email, name=name)
        user.set_password(password)
        user.save()
        return user
