from rest_framework import serializers, validators
from django.contrib.auth import get_user_model
from reviews.models import Title, Category, Genre

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
