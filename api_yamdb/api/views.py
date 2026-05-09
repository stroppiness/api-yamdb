from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Genre, Title, Review, Title
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer, 
    CommentSerializer
)
from .pagination import APIPagination

class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов на произведения."""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = APIPagination

    def get_title(self):
        """Возвращает произведение по title_id из URL."""
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title

    def get_queryset(self):
        """Возвращает все отзывы к произведению."""
        title = self.get_title()
        return title.reviews.all()
    
    def perform_create(self, serializer):
        """Создаёт отзыв, привязывая автора и произведение."""
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев к отзывам."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = APIPagination

    def get_review(self):
        """Возвращает отзыв по review_id и title_id из URL."""
        review = get_object_or_404(
            Review, 
            pk=self.kwargs['review_id'],
            title__pk=self.kwargs['title_id'])
        return review
    
    def get_queryset(self):
        """Возвращает все комментарии к отзыву."""
        review = self.get_review()
        return review.comments.all()
    
    def perform_create(self, serializer):
        """Создаёт комментарий, привязывая автора и отзыв."""
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)


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
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')
    http_method_names = ['get', 'post', 'patch', 'delete']
