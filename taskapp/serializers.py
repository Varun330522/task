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

    def validate(self, data):
        if 'password' in data:
            password = data['password']
            if len(password) < 8:
                raise serializers.ValidationError(
                    "Password must be at least 8 characters long.")
            if not re.match(self.PASSWORD_REGEX, password):
                raise serializers.ValidationError(
                    "Password must meet the complexity requirements.")

        if 'email' in data:
            email = data['email']
            if not re.match(self.EMAIL_REGEX, email):
                raise serializers.ValidationError("Invalid email format.")

        if 'phone_number' in data:
            phone_number = data['phone_number']
            if not re.match(self.PHONE_NUMBER_REGEX, phone_number):
                raise serializers.ValidationError(
                    "Invalid phone number format. Please provide a 10-digit number.")

        return data
