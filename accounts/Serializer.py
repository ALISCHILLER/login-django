from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import MyUser

# Serializer برای ثبت‌نام کاربر
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # فقط برای نوشتن

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError(_('ایمیل نمی‌تواند خالی باشد.'))
        if MyUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('کاربری با این ایمیل قبلاً ثبت‌نام کرده است.'))
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(_('رمز عبور باید حداقل ۸ کاراکتر باشد.'))
        return value

    def create(self, validated_data):
        # ساخت کاربر جدید
        user = MyUser.objects.create_user(**validated_data)
        return user