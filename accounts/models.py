from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


# ==========================
# 🔹 Gestionnaire personnalisé d'utilisateurs
# ==========================
class CustomUserManager(BaseUserManager):
    """
    Manager personnalisé pour gérer la création des utilisateurs et superutilisateurs.
    """

    def create_user(self, email, company_name, phone, password=None, role='user', **extra_fields):
        """
        Crée et retourne un utilisateur normal.
        """
        if not email:
            raise ValueError('Un email est requis')
        if not company_name:
            raise ValueError('Le nom de l’entreprise est requis')
        if not phone:
            raise ValueError('Le numéro de téléphone est requis')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            company_name=company_name,
            phone=phone,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, company_name, phone, password=None, **extra_fields):
        """
        Crée et retourne un superutilisateur (admin).
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, company_name, phone, password, role='admin', **extra_fields)


# ==========================
# 🔹 Rôles disponibles
# ==========================
ROLE_CHOICES = (
    ('user', 'Utilisateur'),
    ('moderator', 'Modérateur'),
    ('admin', 'Administrateur'),
)


# ==========================
# 🔹 Modèle utilisateur personnalisé
# ==========================
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_premium = models.BooleanField(default=False)

    # Champs obligatoires pour Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company_name', 'phone']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.company_name} ({self.role})"

    class Meta:
        ordering = ['-date_joined']
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
