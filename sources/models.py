from django.db import models


class Source(models.Model):
    """Representa uma fonte de notícias, seja um feed RSS ou uma API externa."""

    name = models.CharField(max_length=200)
    url = models.URLField(unique=True) # URL única garante que a mesma fonte não seja cadastrada duas vezes
    is_rss = models.BooleanField(default=False) # False = fonte via API (ex: NewsAPI); True = feed RSS
    is_active = models.BooleanField(default=True) # Permite desativar uma fonte sem excluí-la do banco
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']