from rest_framework import permissions

# 🔹 Permission pour les administrateurs uniquement
class IsAdmin(permissions.BasePermission):
    """Autorise uniquement les utilisateurs ayant le rôle 'admin'."""
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )


# 🔹 Permission pour les modérateurs et administrateurs
class IsModerator(permissions.BasePermission):
    """Autorise les utilisateurs ayant le rôle 'moderator' ou 'admin'."""
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ['moderator', 'admin']
        )


# 🔹 Permission combinée Admin OU Modérateur
class IsAdminOrModerator(permissions.BasePermission):
    """Autorise l'accès si l'utilisateur est admin ou modérateur."""
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ['admin', 'moderator']
        )


# 🔹 Permission pour le propriétaire ou l’administrateur
class IsOwnerOrAdmin(permissions.BasePermission):
    """Autorise l'accès si l'utilisateur est propriétaire ou admin."""
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user
            and request.user.is_authenticated
            and (obj == request.user or request.user.role == 'admin')
        )


# 🔹 Permission pour le propriétaire, modérateur ou administrateur
class IsOwnerOrModeratorOrAdmin(permissions.BasePermission):
    """Autorise l'accès si l'utilisateur est :
       - le propriétaire de l'objet
       - un modérateur
       - un administrateur
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (obj.owner == user or user.role in ['moderator', 'admin'])
        )
