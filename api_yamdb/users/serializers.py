from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации пользователя.

    Используется для эндпоинта /auth/signup/.
    """
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Username не может быть "me"'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже занят")
        return value


class GetUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
