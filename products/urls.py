from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet

# ================================
# Configuration du routeur DRF
# ================================
# Le routeur DRF génère automatiquement toutes les routes
# pour les ViewSets (list, retrieve, create, update, delete)
router = DefaultRouter()

# Route pour la gestion des produits
router.register(
    r'products',            # URL prefix → /api/products/
    ProductViewSet,         # ViewSet associé
    basename='products'     # Nom de référence interne
)

# Route pour la gestion des catégories
router.register(
    r'categories',          # URL prefix → /api/categories/
    CategoryViewSet,        # ViewSet associé
    basename='categories'   # Nom de référence interne
)

# ================================
# URLs de l'application "products"
# ================================
urlpatterns = [
    # On inclut toutes les routes générées par le routeur
    path('', include(router.urls)),
]
