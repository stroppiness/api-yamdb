import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import (IsAdmin, IsAuthorOrModeratorOrAdmin)
from .serializers import (GetUserSerializer, SignupSerializer, TokenSerializer,
                          PostUserSerializer, PatchUserSerializer)

User = get_user_model()


class SelfRegistrationViewSet(viewsets.ViewSet):
    """
    Вьюсет для самостоятельной регистрации пользователя
    с дальнейшей отправкой кода на почту. Для любой роли.

    Используется для эндпоинта /auth/signup/.
    """
    http_method_names = ['post']
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():

            username = serializer.validated_data['username']
            email = serializer.validated_data['email']

            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )

            code = str(random.randint(100000, 999999))
            user.confirmation_code = code
            user.save()

            send_mail(
                subject='Код подтверждения yamdb',
                message=f'Код подтверждения: {code}',
                from_email='yamdb@gmail.com',
                recipient_list=[user.email]
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет изменения данных о пользователях. Для админов.
    """
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_serializer_class(self):

        if self.action == 'list' or self.action == 'retrieve':
            return GetUserSerializer

        if self.action == 'create':
            return PostUserSerializer

        if self.action == 'partial_update':
            return PatchUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для получения данных о пользователях.
    Для админов или модераторов.
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthorOrModeratorOrAdmin]

    def get_serializer_class(self):

        if self.action == 'list' or self.action == 'retrieve':
            return GetUserSerializer

        return PostUserSerializer


class TokenViewSet(viewsets.ViewSet):
    """
    Вьюсет для генерации jwt-токена. Для любой роли.
    """
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def create(self, request):
        serializer = TokenSerializer(data=request.data)

        if serializer.is_valid():

            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']

            user = get_object_or_404(User, username=username)

            if user.confirmation_code != confirmation_code:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
