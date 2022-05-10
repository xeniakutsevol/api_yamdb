from django.shortcuts import render
from rest_framework import viewsets
from rewiews.models import Title, Category, Genre
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer
from rest_framework import mixins 


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, 
                            mixins.ListModelMixin, mixins.DestroyModelMixin, 
                            viewsets.GenericViewSet): 

    pass


class CategoriesViewSet(CreateRetrieveViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenresViewSet(CreateRetrieveViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
