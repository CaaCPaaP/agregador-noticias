from django.db import models
from django.contrib.auth.models import User
from articles.models import Category


class UserPreference(models.Model):
    """Preferências do usuário, criadas automaticamente junto com o cadastro."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE, # Ao excluir o usuário, suas preferências também são removidas
        related_name='preference'
    )
    favorite_categories = models.ManyToManyField(Category, blank=True) # blank=True permite usuários sem categorias favoritas definidas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} preferences'