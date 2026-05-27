from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .models import UserPreference
from .serializers import RegisterSerializer, UserPreferenceSerializer


class RegisterView(generics.CreateAPIView):
    """Endpoint de cadastro. Acessível sem autenticação."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserPreferenceView(generics.RetrieveUpdateAPIView):
    """Leitura e atualização das preferências do usuário autenticado."""

    serializer_class = UserPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.preference