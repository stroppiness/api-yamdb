from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Review, Title
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from .pagination import APIPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = APIPagination

    def get_title(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()
    
    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = APIPagination

    def get_review(self):
        review = get_object_or_404(
            Review, 
            pk=self.kwargs['review_id'],
            title__pk=self.kwargs['title_id'])
        return review
    
    def get_queryset(self):

        review = self.get_review()
        return review.comments.all()
    
    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)