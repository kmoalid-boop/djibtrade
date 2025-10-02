from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Category(models.Model):
    """
    Modèle représentant une catégorie de produits.
    Exemple : 'Huiles végétales', 'Farine', 'Boissons', etc.
    """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Modèle représentant une annonce de produit publiée par un utilisateur.
    """

    # --- Constantes ---
    CURRENCY_CHOICES = [
        ('DJF', 'Franc Djiboutien'),
        ('USD', 'Dollar Américain'),
    ]

    CONTACT_METHOD_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('phone', 'Téléphone'),
        ('both', 'WhatsApp et Téléphone'),
    ]

    # --- Relations ---
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="Utilisateur qui a créé l'annonce."
    )

    # --- Informations principales ---
    title = models.CharField(max_length=255, help_text="Nom du produit")
    description = models.TextField(blank=True, null=True, help_text="Description du produit")

    # --- Prix et devise ---
    unit_price = models.PositiveIntegerField(  # ← CHANGEMENT ICI : Decimal → PositiveInteger
        validators=[MinValueValidator(1)],  # Prix minimum 1 DJF
        help_text="Prix unitaire en Francs Djiboutiens"
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='DJF',
        help_text="Devise du prix"
    )
    stock = models.PositiveIntegerField(default=1, help_text="Quantité disponible")
    total_price = models.PositiveIntegerField(  # ← CHANGEMENT ICI : Decimal → PositiveInteger
        blank=True,
        null=True,
        help_text="Prix total calculé automatiquement"
    )

    # --- Classification ---
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Catégorie du produit"
    )
    city = models.CharField(max_length=100, blank=True, null=True, help_text="Ville de disponibilité")

    # --- Médias ---
    image = models.ImageField(
        upload_to='products/', 
        default='products/default_product.jpg',
        help_text="Image du produit"
    )

    # --- Contact ---
    contact_method = models.CharField(
        max_length=20, 
        choices=CONTACT_METHOD_CHOICES, 
        default='whatsapp',
        help_text="Méthode de contact préférée"
    )
    whatsapp_contact = models.CharField(max_length=20, blank=True, null=True, help_text="Numéro WhatsApp")
    phone_contact = models.CharField(max_length=20, blank=True, null=True, help_text="Numéro de téléphone")

    # --- Liens externes ---
    whatsapp_link = models.URLField(max_length=255, blank=True, null=True, help_text="Lien direct WhatsApp")

    # --- Statistiques ---
    views = models.PositiveIntegerField(default=0, help_text="Nombre de vues")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date de création de l'annonce")

    def save(self, *args, **kwargs):
        """
        - Calcule automatiquement le prix total = unit_price × stock.
        - Génère automatiquement le lien WhatsApp si l'utilisateur a un numéro de téléphone.
        """
        # Calcul automatique du prix total (maintenant en entier)
        if self.unit_price and self.stock:
            self.total_price = self.unit_price * self.stock
        else:
            self.total_price = None

        # Génération automatique du lien WhatsApp
        if self.owner and hasattr(self.owner, 'phone') and self.owner.phone:
            phone_number = str(self.owner.phone).replace(" ", "").replace("+", "")
            self.whatsapp_link = f"https://wa.me/{phone_number}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title