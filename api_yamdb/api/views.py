from django.shortcuts import render
from rest_framework import viewsets
from reviews.models import Title, Category, Genre
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer
from rest_framework import mixins 


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer    
#Это в процессе



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

