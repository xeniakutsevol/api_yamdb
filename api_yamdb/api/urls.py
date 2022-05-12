from django.urls import include, path
from rest_framework import routers
from .views import (SignUpViewSet, UsersAdminViewSet, obtain_token,
                    CategoriesViewSet, GenresViewSet, TitlesViewSet)


app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register('auth/signup', SignUpViewSet, basename='signup')
v1_router.register('users', UsersAdminViewSet, basename='usersadmin')
v1_router.register(r'categories', CategoriesViewSet, basename='categories')
v1_router.register(r'genres', GenresViewSet, basename='genres')
v1_router.register(r'titles', TitlesViewSet, basename='titles')


urlpatterns = [
    path('auth/token/', obtain_token),
    path('', include(v1_router.urls)),
]
