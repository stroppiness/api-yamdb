from datetime import date

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
