from rest_framework import serializers

from .models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True,
                            read_only=True)
    rating = serializers.IntegerField(read_only=True,
                                      default=None)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = fields


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        from datetime import date
        if value > date.today().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего.'
            )
        return value
