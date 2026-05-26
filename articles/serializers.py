from rest_framework import serializers
from .models import Article, Category
from sources.serializers import SourceSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ArticleSerializer(serializers.ModelSerializer):
    source = SourceSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'url', 'description',
            'author', 'image_url', 'source', 'category',
            'published_at', 'created_at'
        ]
        read_only_fields = ['created_at']