from rest_framework import serializers, validators
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
        fields = ('username', 'email', 'role')
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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate(self, attrs):
        if not self.context['request'].method == 'POST':
            return attrs
        author = self.context['request'].user
        title = self.context['request'].parser_context['view'].kwargs.get(
            'title_id')
        if Review.objects.filter(title=title, author=author).exist():
            raise serializers.ValidationError(
                'Вы можете написать только один отзыв на произведение'
            )
        return attrs

    class Meta:
        fields = '__all__'
        model = Review
        unique_together = ('author', 'title')
        extra_kwargs = {
            'title_id': {
                'valiators': [
                    validators.UniqueValidator(
                        queryset=User.objects.all())
                ]
            },
            'author':{
                'valiators': [
                    validators.UniqueValidator(
                        queryset=User.objects.all())
                ]
            },
        }
