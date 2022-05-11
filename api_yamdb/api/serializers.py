from rest_framework import serializers

from reviews.models import Title, Category, Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='titles',
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre



