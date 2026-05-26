from django.db import models
from sources.models import Source


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'


class Article(models.Model):
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    author = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(blank=True, max_length=2000)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at']