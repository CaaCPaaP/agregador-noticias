from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserPreference
from articles.serializers import CategorySerializer


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserPreference.objects.create(user=user)
        return user


class UserPreferenceSerializer(serializers.ModelSerializer):
    favorite_categories = CategorySerializer(many=True, read_only=True)
    favorite_category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        source='favorite_categories',
        queryset=__import__('articles.models', fromlist=['Category']).Category.objects.all()
    )

    class Meta:
        model = UserPreference
        fields = ['id', 'favorite_categories', 'favorite_category_ids', 'updated_at']
        read_only_fields = ['updated_at']