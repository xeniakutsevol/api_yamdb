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

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
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
        queryset = Genre.objects,
        slug_field = 'slug',
        many=True
    )

    category = serializers.SlugRelatedField(
        queryset = Category.objects,
        slug_field = 'slug'
    )

    class Meta:
        fields = '__all__'
        model = Title
