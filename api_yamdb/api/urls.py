from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AdminUserViewSet, CategoryViewSet, CommentViewSet,
                    GenreViewSet, MeUserView, ReviewViewSet,
                    SelfRegistrationViewSet, TitleViewSet, TokenViewSet)

router = DefaultRouter()
router.register('auth/signup', SelfRegistrationViewSet, basename='signup')
router.register('users', AdminUserViewSet)
router.register('auth/token', TokenViewSet, basename='token')
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='title-reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='review-comments'
)

urlpatterns = [
    path('users/me/', MeUserView.as_view()),
    path('', include(router.urls)),
]
