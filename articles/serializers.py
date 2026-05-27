from rest_framework import serializers
from .models import Article, Category
from sources.serializers import SourceSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Serializer de leitura e escrita para categorias."""

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer somente leitura para artigos.
    
    Expande source e category como objetos completos
    em vez de retornar apenas seus IDs.
    """

    source = SourceSerializer(read_only=True) # Retorna objeto completo da fonte, não apenas o ID
    category = CategorySerializer(read_only=True) # Retorna objeto completo da categoria, não apenas o ID

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'url', 'description',
            'author', 'image_url', 'source', 'category',
            'published_at', 'created_at'
        ]
        read_only_fields = ['created_at']