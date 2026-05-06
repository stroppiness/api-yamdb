from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации пользователя.

    Используется для эндпоинта /auth/signup/.

    Создаёт нового пользователя в системе.
    """
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')
