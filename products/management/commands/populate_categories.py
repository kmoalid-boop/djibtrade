from django.core.management.base import BaseCommand
from products.models import Category

class Command(BaseCommand):
    help = "Réinitialise et insère les catégories par défaut pour les grossistes à Djibouti"

    def handle(self, *args, **kwargs):
        # Supprimer toutes les anciennes catégories
        Category.objects.all().delete()
        self.stdout.write(self.style.WARNING("🗑️ Toutes les anciennes catégories ont été supprimées."))

        # Liste des nouvelles catégories
        categories = [
            "Huiles végétales & graisses",
            "Véhicules & pièces détachées",
            "Fer, acier & métaux industriels",
            "Sucres & produits sucrés",
            "Céréales & produits céréaliers",
            "Produits plastiques & dérivés",
            "Électronique & équipements électriques",
            "Aliments emballés / secs (farine, riz, etc.)",
            "Huile comestible (palme, tournesol)",
            "Produits pétroliers & lubrifiants",
            "Matériaux de construction (sable, ciment, ferraille)",
            "Sel & produits miniers",
            "Produits pharmaceutiques, hygiène & santé",
            "Produits de pêche / fruits de mer",
            "Textiles & vêtements en gros",
            "Accessoires auto & lubrifiants",
            "Fournitures de bureau & papeterie",
            "Produits ménagers & nettoyants"
        ]

        # Insertion des nouvelles catégories
        for cat in categories:
            Category.objects.create(name=cat)

        self.stdout.write(self.style.SUCCESS("✅ Les catégories ont été réinitialisées et insérées avec succès."))
