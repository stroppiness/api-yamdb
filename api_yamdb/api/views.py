from django.db.models import Avg
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Genre, Title
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет для категорий: список, создание, удаление."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет для жанров: список, создание, удаление."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений без PUT."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).select_related('category').prefetch_related('genre')

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer
