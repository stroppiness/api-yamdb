from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Review, Title
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from .pagination import APIPagination


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов на произведения."""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = APIPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

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
    http_method_names = ['get', 'post', 'patch', 'delete']

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