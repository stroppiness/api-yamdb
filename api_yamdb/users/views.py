import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.response import Response

from .permissions import (IsAdmin, IsAuthorOrModeratorOrAdmin,
                          ReadOnlyOrAuthenticated)
from .serializers import (GetUserSerializer, SignupSerializer,
                          UpdateUserSerializer)

User = get_user_model()


class SelfRegistrationViewSet(viewsets.ViewSet):
    """
    Вьюсет для самостоятельной регистрации пользователя
    с дальнейшей отправкой кода на почту.

    Используется для эндпоинта /auth/signup/.
    """
    http_method_names = ['post']

    def create(self, request):
        serializer = SignupSerializer(data=request.data)
        self.permission_classes = [ReadOnlyOrAuthenticated]

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
    queryset = User.objects.all()
    permission_classes = [IsAdmin]

    def get_serializer_class(self):

        if self.action == 'list' or self.action == 'retrieve':
            return GetUserSerializer

        return UpdateUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthorOrModeratorOrAdmin]

    def get_serializer_class(self):

        if self.action == 'list' or self.action == 'retrieve':
            return GetUserSerializer

        return UpdateUserSerializer
