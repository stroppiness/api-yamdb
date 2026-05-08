from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (AdminUserViewSet, SelfRegistrationViewSet, TokenViewSet,
                    UserViewSet)

router = SimpleRouter()
router.register(r'auth/signup', SelfRegistrationViewSet, basename='signup')
router.register('users', AdminUserViewSet)
router.register(r'users/me', UserViewSet, basename='me')
router.register(r'auth/token', TokenViewSet, basename='token')

urlpatterns = [
    path('', include(router.urls)),
]
