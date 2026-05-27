from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Article, Category
from sources.models import Source

User = get_user_model()

class ArticleAPITestCase(TestCase):
    def setUp(self):
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
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_retrieve_article(self):
        response = self.client.get(f'/api/articles/{self.article.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'].lower(), 'artigo de teste')
    
    def test_filter_by_category(self):
        response = self.client.get(f'/api/articles/?category={self.category.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_search_articles(self):
        response = self.client.get('/api/articles/?search=teste')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_search_no_results(self):
        response = self.client.get('/api/articles/?search=inexistente')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
    

class AuthAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        response = self.client.post('/api/auth/register/',{
            'username': 'novousuario',
            'email': 'novo@email.com',
            'password': 'senha1234'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'novousuario')
        self.assertNotIn('password', response.data)

    def test_login_user(self):
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
        User.objects.create_user(
            username = 'usuario',
            password = 'senha1234'
        )
        response = self.client.post('/api/auth/login/', {
            'username': 'usuario',
            'password': 'senhaerrada'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        