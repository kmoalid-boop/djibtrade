from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les produits.
    - List et Retrieve : accessible à tous
    - Create, Update, Delete : réservé aux utilisateurs authentifiés
    - Filtrage par catégorie : /products/?category=<id>
    """
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_permissions(self):
        """Définit les permissions en fonction de l'action."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Filtrage par catégorie si ?category=<id> est passé en paramètre.
        """
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def perform_create(self, serializer):
        """
        L'utilisateur choisit sa devise lors de la création.
        Si aucune devise n'est envoyée, 'DJF' est utilisée par défaut (défini dans le modèle).
        """
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """
        Modification autorisée uniquement pour :
        - Le propriétaire de l'annonce
        - Les modérateurs
        - Les superadmins
        """
        product = self.get_object()
        user = self.request.user
        if user.role == 'moderator' or user.is_superuser or product.owner == user:
            serializer.save()
        else:
            raise PermissionDenied("Vous n'avez pas la permission de modifier cette annonce.")

    def perform_destroy(self, instance):
        """
        Suppression autorisée uniquement pour :
        - Le propriétaire
        - Les modérateurs
        - Les superadmins
        """
        user = self.request.user
        if user.role == 'moderator' or user.is_superuser or instance.owner == user:
            instance.delete()
        else:
            raise PermissionDenied("Vous n'avez pas la permission de supprimer cette annonce.")

    def retrieve(self, request, *args, **kwargs):
        """
        Lorsqu'un produit est consulté, on incrémente le compteur de vues.
        """
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les catégories.
    Accessible en lecture seule à tout le monde.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
