from rest_framework import viewsets, permissions
from .models import Source
from .serializers import SourceSerializer


class SourceViewSet(viewsets.ModelViewSet):
    """CRUD de fontes de notícias.
    
    Leitura pública. Criação, edição e exclusão restritas a admins.
    """

    queryset = Source.objects.filter(is_active=True) # Exclui fontes inativas da listagem
    serializer_class = SourceSerializer

    def get_permissions(self):
        # Qualquer pessoa pode listar e visualizar fontes
        # Apenas admins podem criar, editar ou excluir
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]