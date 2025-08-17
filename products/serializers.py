from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les catégories de produits.
    """
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les annonces de produits.
    """
    owner_name = serializers.SerializerMethodField(read_only=True)  # Nom du propriétaire
    category_name = serializers.CharField(source='category.name', read_only=True)  # Nom de la catégorie

    class Meta:
        model = Product
        fields = [
            'id',
            'owner_name',
            'title',
            'description',
            'unit_price',
            'currency',
            'quantity',
            'total_price',
            'category',
            'category_name',
            'city',
            'image',
            'whatsapp_link',
            'views',
            'created_at',
        ]
        read_only_fields = ['owner_name', 'total_price', 'whatsapp_link', 'views', 'created_at']

    def get_owner_name(self, obj):
        """
        Retourne le nom complet de l'utilisateur si disponible,
        sinon son identifiant.
        """
        return getattr(obj.owner, 'full_name', str(obj.owner))

    def validate_currency(self, value):
        """
        Validation personnalisée : assure que la devise est DJF ou USD.
        """
        valid_currencies = [choice[0] for choice in Product.CURRENCY_CHOICES]
        if value not in valid_currencies:
            raise serializers.ValidationError("La devise doit être DJF ou USD.")
        return value

    def create(self, validated_data):
        """
        Création du produit :
        - L'owner est défini automatiquement depuis la requête.
        - Le prix total est calculé automatiquement par le modèle.
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['owner'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Mise à jour du produit :
        - Le prix total est recalculé automatiquement.
        """
        return super().update(instance, validated_data)
