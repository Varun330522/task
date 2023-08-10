from rest_framework import serializers
from .models import UserDetails
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = "__all__"

    PASSWORD_REGEX = r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
    EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    PHONE_NUMBER_REGEX = r'^\d{10}$'

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long.")
        if not re.match(self.PASSWORD_REGEX, value):
            raise serializers.ValidationError(
                "Password must meet the complexity requirements.")
        return value

    def validate_email(self, value):
        if not re.match(self.EMAIL_REGEX, value):
            raise serializers.ValidationError("Invalid email format.")
        return value
