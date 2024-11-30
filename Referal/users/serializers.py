from rest_framework import serializers
from .models import PhoneNumberVerification
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class PhoneNumberVerificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PhoneNumberVerification
        fields = ["phone_number", "user"]
