import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import (CharFilter, DjangoFilterBackend,
                                           FilterSet)
from rest_framework import filters, mixins, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title

from .pagination import APIPagination
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrModeratorOrAdmin
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetUserSerializer,
                          MePostUserSerializer, PatchUserSerializer,
                          PostUserSerializer, ReviewSerializer,
                          SignupSerializer, TitleSerializer, TokenSerializer)

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
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):

        if self.action == 'list' or self.action == 'retrieve':
            return GetUserSerializer

        if self.action == 'create':
            return PostUserSerializer

        if self.action == 'partial_update':
            return PatchUserSerializer

        return GetUserSerializer


class MeUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = GetUserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = MePostUserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


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


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов на произведения."""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrModeratorOrAdmin]
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
    permission_classes = [IsAuthorOrModeratorOrAdmin]
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


class TitleFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    name = CharFilter(field_name='name', lookup_expr='contains')
    year = CharFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year')


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений без PUT."""

    queryset = Title.objects.select_related(
        'category').prefetch_related(
            'genre').annotate(
        rating=Avg('reviews__score')
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']
