from rest_framework import generics, status, permissions, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.password_validation import validate_password
from .models import User
from .serializers import UserSerializer, ChangePasswordSerializer
from .permissions import IsAdmin, IsModerator, IsAdminOrModerator, IsOwnerOrAdmin


# 🔹 Inscription d'un nouvel utilisateur
class RegisterView(generics.CreateAPIView):
    """
    Permet à n'importe qui de s'enregistrer.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


# 🔹 Profil utilisateur connecté (lecture et mise à jour)
class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Récupère et met à jour le profil de l'utilisateur connecté.
    L'utilisateur doit être connecté et propriétaire ou admin.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self):
        return self.request.user


# 🔹 Changement de mot de passe
class ChangePasswordView(APIView):
    """
    Permet à l'utilisateur connecté de changer son mot de passe.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        # Vérifie le mot de passe actuel
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {"old_password": ["Mot de passe actuel incorrect"]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Valide le nouveau mot de passe
        try:
            validate_password(serializer.validated_data['new_password'], user)
        except Exception as e:
            return Response({"new_password": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        # Applique le nouveau mot de passe
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({"detail": "Mot de passe changé avec succès"}, status=status.HTTP_200_OK)


# 🔹 Liste et gestion des utilisateurs (admin/modérateur)
class UserViewSet(viewsets.ModelViewSet):
    """
    Gestion complète des utilisateurs.
    - Liste et détail : admin et modérateurs
    - Suppression et modification : admin uniquement
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Règles de permission en fonction de l'action.
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated(), IsAdminOrModerator()]
        elif self.action in ['destroy', 'update', 'partial_update']:
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]

    # 🔹 Recherche et filtrage par email, nom ou rôle
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['email', 'company_name', 'role']
    ordering_fields = ['date_joined', 'company_name']
    ordering = ['-date_joined']
