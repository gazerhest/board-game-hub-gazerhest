from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        error_messages={
            "required": "Поле є обов'язковим.",
            "max_length": "К-сть символів не може перевищувати 150."
        }
    )
    first_name = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=150
    )
    last_name = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=150
    )
    email = serializers.EmailField(
        required=True,
        max_length=123,
        error_messages={
            "required": "Поле є обов'язковим.",
            "invalid": "Некоректна електронна пошта",
        }
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        max_length=167,
        error_messages={
            "required": "Поле є обов'язковим.",
            "min_length": "Мінімальна к-сть символів - 8",
            "max_length": "Максимальна к-сть символів - 167"
        }
    )
    password_confirmation = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        max_length=167,
        error_messages={
            "required": "Поле є обов'язковим.",
        }
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_confirmation']

    def validate_email(self, val):
        if User.objects.filter(email__iexact=val).exists():
            raise serializers.ValidationError("Користувач з таким email уже існує")
        return val

    def validate_username(self, val):
        if User.objects.filter(email__iexact=val).exists():
            raise serializers.ValidationError("Користувач з таким user name уже існує")
        return val

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password_confirmation"):
            raise serializers.ValidationError({"password_confirmation": "Паролі не співпадають"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user
    