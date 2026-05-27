from rest_framework import serializers
from .models import Source


class SourceSerializer(serializers.ModelSerializer):
    """Serializer de leitura e escrita para fontes de notícias."""

    class Meta:
        model = Source
        fields = ['id', 'name', 'url', 'is_rss', 'is_active', 'created_at']
        read_only_fields = ['created_at'] # Preenchido automaticamente pelo banco