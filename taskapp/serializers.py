from rest_framework import serializers
from .models import UserDetails, Loan
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = "__all__"

    PASSWORD_REGEX = r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
    EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

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


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    PASSWORD_REGEX = r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
    EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

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


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["loan_id", "user_id", "amount", "tenure_month", "status"]
