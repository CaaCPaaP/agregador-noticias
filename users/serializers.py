from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserPreference
from articles.serializers import CategorySerializer


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para cadastro de novos usuários.
    
    Cria o usuário e seu UserPreference automaticamente.
    """

    password = serializers.CharField(
        write_only=True,  # Garante que a senha nunca apareça em nenhuma resposta da API
        min_length=8
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # create_user garante que a senha seja armazenada como hash, nunca em texto puro
        user = User.objects.create_user(**validated_data)
        UserPreference.objects.create(user=user)
        return user


class UserPreferenceSerializer(serializers.ModelSerializer):
    """Serializer para leitura e atualização das preferências do usuário.
    
    Usa dois campos para o mesmo relacionamento:
    - favorite_categories: leitura, retorna objetos completos
    - favorite_category_ids: escrita, aceita apenas IDs (mais simples para o cliente)
    """

    favorite_categories = CategorySerializer(many=True, read_only=True)
    favorite_category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True, # Só aceita IDs na escrita; na leitura usa favorite_categories
        source='favorite_categories',
        queryset=__import__('articles.models', fromlist=['Category']).Category.objects.all()
    )

    class Meta:
        model = UserPreference
        fields = ['id', 'favorite_categories', 'favorite_category_ids', 'updated_at']
        read_only_fields = ['updated_at']