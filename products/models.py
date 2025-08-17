from django.db import models
from django.conf import settings


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
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Prix unitaire")
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='DJF',
        help_text="Devise du prix"
    )
    quantity = models.PositiveIntegerField(default=1, help_text="Quantité disponible")
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
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
    image = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Image du produit")

    # --- Liens externes ---
    whatsapp_link = models.URLField(max_length=255, blank=True, null=True, help_text="Lien direct WhatsApp")

    # --- Statistiques ---
    views = models.PositiveIntegerField(default=0, help_text="Nombre de vues")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date de création de l'annonce")

    def save(self, *args, **kwargs):
        """
        - Calcule automatiquement le prix total = unit_price × quantity.
        - Génère automatiquement le lien WhatsApp si l'utilisateur a un numéro de téléphone.
        """
        # Calcul automatique du prix total
        if self.unit_price and self.quantity:
            self.total_price = self.unit_price * self.quantity

        # Génération automatique du lien WhatsApp
        if self.owner and hasattr(self.owner, 'phone') and self.owner.phone:
            phone_number = str(self.owner.phone).replace(" ", "").replace("+", "")
            self.whatsapp_link = f"https://wa.me/{phone_number}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
