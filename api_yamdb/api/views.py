from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, mixins, filters
from django.contrib.auth import get_user_model
from .serializers import (SignUpSerializer, UserAdminSerializer,
                          CommentSerializer, ReviewSerializer,
                          TitleReadSerializer, CategorySerializer,
                          GenreSerializer, TitleWriteSerializer,
                          UserAdminPatchSerializer)
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes, action
from .permissions import ReviewCommentPermission, UserAdminPermission
from reviews.models import Title, Category, Genre, Review
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TitleFilter


User = get_user_model()


class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers=headers)

    def perform_create(self, serializer):
        serializer.save()
        user = get_object_or_404(
            User, username=serializer.validated_data.get('username'))
        token = default_token_generator.make_token(user=user)
        serializer.save(confirmation_code=token)
        send_mail(subject='Confirmation code', message=token,
                  from_email='YaMBD',
                  recipient_list=(serializer.validated_data.get('email'),))


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def obtain_token(request):
    if 'username' in request.data and 'confirmation_code' in request.data:
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        refresh = RefreshToken.for_user(user)
        if default_token_generator.check_token(user, confirmation_code):
            return Response(status=200, data=str(refresh.access_token))
    return Response(status=400)


class UsersAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, UserAdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=True,
        url_path='me'
    )
    def get_object(self):
        if self.kwargs.get('username') == 'me':
            return self.request.user
        return super(UsersAdminViewSet, self).get_object()

    def destroy(self, request, *args, **kwargs):
        if self.kwargs.get('username') == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if (self.request.method == 'PATCH'
           and self.kwargs.get('username') == 'me'):
            return UserAdminPatchSerializer
        return UserAdminSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            mixins.ListModelMixin, mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):

    pass


class CategoriesViewSet(CreateRetrieveViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(CreateRetrieveViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReviewCommentPermission,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        #return Review.objects.filter(title=title)
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        author = self.request.user
        serializer.save(author=author, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id'))
           # title__id=self.kwargs.get('title_id'))
        return review.comments.all()
       # title_id = self.kwargs['title_id']
       # review_id = self.kwargs['review_id']
       # review = get_object_or_404(
           # Review.objects.filter(title_id=title_id),
           # pk=review_id
       # )
       # return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id'))
            #title__id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)
