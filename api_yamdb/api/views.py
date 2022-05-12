from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, mixins
from django.contrib.auth import get_user_model
from .serializers import (SignUpSerializer, UserAdminSerializer,
                          TitleSerializer, CategorySerializer, GenreSerializer)
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view, permission_classes
from .permissions import UserAdminPermission
from reviews.models import Title, Category, Genre

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
    serializer_class = UserAdminSerializer
    permission_classes = (UserAdminPermission,)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
# Это в процессе


class CreateRetrieveViewSet(mixins.RetrieveModelMixin,
                            mixins.ListModelMixin, mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):

    pass


class CategoriesViewSet(CreateRetrieveViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenresViewSet(CreateRetrieveViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
