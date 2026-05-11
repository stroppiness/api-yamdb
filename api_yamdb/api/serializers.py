from datetime import date

from django.core.validators import RegexValidator
from django.db.models import Q
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User


class SignupSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации пользователя.
    """
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
            )
        ]
    )
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Username не может быть "me"'
            )
        return value

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(
            Q(username=username) & ~Q(email=email)
            | ~Q(username=username) & Q(email=email)
        ).exists():

            raise serializers.ValidationError('Username или email существует')

        return data


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
    email = serializers.EmailField(max_length=254, required=True)
    last_name = serializers.CharField(max_length=150, required=False)
    first_name = serializers.CharField(max_length=150, required=False)

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


class MePostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
        )
        read_only_fields = ('role',)


class TokenSerializer(serializers.ModelSerializer):
    """
    Сериализатор получения токена.
    """
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            title = self.context['view'].get_title()

            if Review.objects.filter(
                title=title,
                author=request.user
            ).exists():
                raise serializers.ValidationError('Вы уже оставили отзыв')

        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        exclude = ('review',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['genre'] = GenreSerializer(instance.genre.all(),
                                                  many=True).data
        return representation

    def validate_year(self, value):
        if value > date.today().year:
            raise serializers.ValidationError(
                'Год не может быть больше текущего.'
            )
        return value
