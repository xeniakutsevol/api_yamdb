from rest_framework import serializers, validators
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from reviews.models import Title, Category, Genre, Comment
from reviews.models import Review, Title

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')
        extra_kwargs = {
            'username': {
                'validators': [
                    validators.UniqueValidator(
                        queryset=User.objects.all()
                    )
                ]
            },
            'email': {
                'validators': [
                    validators.UniqueValidator(
                        queryset=User.objects.all()
                    )
                ]
            }
        }

    def validate_username(self, data):
        if data == 'me':
            raise serializers.ValidationError('Невалидный username.')
        return data


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'bio', 'first_name',
                  'last_name')
        extra_kwargs = {
            'username': {
                'validators': [
                    validators.UniqueValidator(
                        queryset=User.objects.all()
                    )
                ]
            },
            'email': {
                'validators': [
                    validators.UniqueValidator(
                        queryset=User.objects.all()
                    )
                ]
            }
        }

    def validate_username(self, data):
        if data == 'me':
            raise serializers.ValidationError('Невалидный username.')
        return data


class UserAdminPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'bio', 'first_name',
                  'last_name')
        extra_kwargs = {
            'role': {'read_only': True},
            'username': {
                'validators': [
                    validators.UniqueValidator(
                        queryset=User.objects.all()
                    )
                ]
            },
            'email': {
                'validators': [
                    validators.UniqueValidator(
                        queryset=User.objects.all()
                    )
                ]
            }
        }

    def validate_username(self, data):
        if data == 'me':
            raise serializers.ValidationError('Невалидный username.')
        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'slug',]
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    #rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        exclude =('review',)
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )

    def validate(self, attrs):
        is_exist = Review.objects.filter(
            author=self.context['request'].user,
            title=get_object_or_404(
                Title,
                pk=self.context['view'].kwargs.get('title_id'))).exists()
        if is_exist and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Вы можете написать только один отзыв на произведение'
            )
        return attrs


    class Meta:
        fields = '__all__'
        model = Review
