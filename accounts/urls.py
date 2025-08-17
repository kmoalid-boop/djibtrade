from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, ProfileView, ChangePasswordView, UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

# Router pour ViewSets
router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    # Authentification et gestion de compte
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # Profil utilisateur connecté
    path('profile/', ProfileView.as_view(), name='profile'),

    # Mot de passe
    path('auth/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('auth/password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    # Router DRF
    path('', include(router.urls)),
]
