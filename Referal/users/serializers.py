from rest_framework import serializers
from .models import PhoneNumberVerification
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class PhoneNumberVerificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Устанавливаем поле user только для чтения

    class Meta:
        model = PhoneNumberVerification
        # fields = ["phone_number", "auth_code", "referal_number", "activated_referal_number", "country_code", "user"]
        fields = ["phone_number", "referal_number", "user"]

    def create(self, validated_data):
        user_data = validated_data.pop("user", None)  # Извлекаем данные пользователя, если они есть
        phone_number_verification = PhoneNumberVerification.objects.create(**validated_data)

        # Создаем пользователя, если данные пользователя переданы
        if user_data:
            user = User.objects.create(**user_data)
            phone_number_verification.user = user
            phone_number_verification.save()

        return phone_number_verification
