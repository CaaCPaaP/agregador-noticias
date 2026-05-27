from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD de categorias.
    
    Leitura pública. Criação, edição e exclusão restritas a admins.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """Listagem e detalhe de artigos. Somente leitura — artigos são criados apenas pelo Celery.
    
    Suporta filtro por source e category, busca por texto e ordenação.
    """

    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['source', 'category']
    search_fields = ['title', 'description', 'author']
    ordering_fields = ['published_at', 'created_at']
    ordering = ['-published_at']

    def get_queryset(self):
        # select_related evita o problema N+1: sem ele, cada artigo faria queries separadas para buscar source e category
        return Article.objects.select_related('source', 'category').all()