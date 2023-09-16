from rest_framework import serializers
from globals.serializers import DynamicFieldsModelSerializer

from .models import CustomUser


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ["password"]
        depth = 2


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(max_length=255)

    def validate(self, data):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not (username or email):
            raise serializers.ValidationError("Either username or email is required.")

        user = None

        if username:
            user = CustomUser.objects.filter(username=username).first()

        if not user and email:
            user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise serializers.ValidationError("User does not exist.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password.")

        data["user"] = user
        return data
