from django.db import models
from sources.models import Source


class Category(models.Model):
    """Categoria temática dos artigos (ex: Tecnologia, Economia)."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True) # Versão da categoria para uso em URLs (ex: 'tecnologia')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'


class Article(models.Model):
    """Artigo coletado de uma fonte de notícias."""

    title = models.CharField(max_length=500)
    url = models.URLField(unique=True) # URL única é usada para deduplicação — evita salvar o mesmo artigo duas vezes
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    author = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(blank=True, max_length=2000) # max_length=2000 porque URLs de imagens de APIs externas frequentemente ultrapassam o padrão de 200 caracteres
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, # SET_NULL preserva o artigo mesmo se a categoria for excluída
        null=True,
        blank=True,
        related_name='articles'
    )
    related_name='articles'
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at'] # Mais recentes primeiro