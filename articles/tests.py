from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Article, Category
from sources.models import Source

# get_user_model() é preferível a importar User diretamente, pois funciona mesmo se o projeto usar um modelo de usuário customizado
User = get_user_model()

class ArticleAPITestCase(TestCase):
    """Testes dos endpoints de artigos e categorias."""

    def setUp(self):
        """Cria dados base reutilizados em todos os testes desta classe.
        
        O Django recria o banco de teste a cada execução,
        então esses dados existem apenas durante os testes.
        """

        self.client = APIClient()
        self.source = Source.objects.create(
            name = 'fonte teste',
            url = 'https://fonte-teste.com',
            is_rss = False,
            is_active = True
        )
        self.category = Category.objects.create(
            name = 'Tecnologia',
            slug = 'tecnologia'
        )
        self.article = Article.objects.create(
            title = 'Artigo de Teste',
            url = 'https://fonte-teste.com/artigo1',
            description = 'Descrição do artigo de teste.',
            source = self.source,
            category = self.category,
        )

    def test_list_articles(self):
        """Verifica se a listagem retorna os artigos com paginação."""

        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_retrieve_article(self):
        """Verifica se o detalhe de um artigo retorna os dados corretos."""

        response = self.client.get(f'/api/articles/{self.article.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'].lower(), 'artigo de teste') # Comparação em lowercase pois alguns bancos retornam texto normalizado
    
    def test_filter_by_category(self):
        """Verifica se o filtro por categoria retorna apenas artigos da categoria."""

        response = self.client.get(f'/api/articles/?category={self.category.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_search_articles(self):
        """Verifica se a busca por palavra-chave encontra artigos pelo título."""

        response = self.client.get('/api/articles/?search=teste')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_search_no_results(self):
        """Verifica se a busca retorna lista vazia quando não há resultados."""

        response = self.client.get('/api/articles/?search=inexistente')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
    

class AuthAPITestCase(TestCase):
    """Testes dos endpoints de autenticação."""

    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        """Verifica se o cadastro cria o usuário e não expõe a senha na resposta."""

        response = self.client.post('/api/auth/register/',{
            'username': 'novousuario',
            'email': 'novo@email.com',
            'password': 'senha1234'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'novousuario')
        self.assertNotIn('password', response.data) # Garante que o campo password nunca apareça na resposta da API

    def test_login_user(self):
        """Verifica se o login retorna os tokens de acesso e refresh."""

        User.objects.create_user(
            username = 'usuario',
            password = 'senha1234'
        )
        response = self.client.post('/api/auth/login/', {
            'username': 'usuario',
            'password': 'senha1234'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_wrong_password(self):
        """Verifica se o login com senha errada retorna 401 Unauthorized."""
        
        User.objects.create_user(
            username = 'usuario',
            password = 'senha1234'
        )
        response = self.client.post('/api/auth/login/', {
            'username': 'usuario',
            'password': 'senhaerrada'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        