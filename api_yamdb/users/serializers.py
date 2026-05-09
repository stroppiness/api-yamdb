from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации пользователя.
    """
    username = serializers.CharField(max_length=254, required=True)
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


class GetUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор получения данных о пользователях.
    """

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


class PostUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор изменения пользовательских данных методом POST.
    """
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

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Email уже зарегистрирован.'
            )
        return value


class PatchUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор изменения пользовательских данных методом PATCH.
    """

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


class TokenSerializer(serializers.ModelSerializer):
    """
    Сериализатор получения токена.
    """
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
