from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


# 🔹 Sérializer principal pour l'utilisateur
class UserSerializer(serializers.ModelSerializer):
    """
    Sérializer pour créer et afficher les utilisateurs.
    - Le mot de passe est write_only pour ne jamais l'exposer.
    - Les champs 'role' et 'is_premium' sont read-only pour empêcher la modification par l'utilisateur.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=6,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'id', 'email', 'company_name', 'logo', 'phone',
            'address', 'city', 'is_premium', 'role', 'password'
        ]
        read_only_fields = ['role', 'is_premium']

    def create(self, validated_data):
        """
        Création sécurisée de l'utilisateur avec mot de passe hashé.
        """
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Mise à jour sécurisée de l'utilisateur.
        - Si un mot de passe est fourni, il est hashé.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance


# 🔹 Sérializer pour le changement de mot de passe
class ChangePasswordSerializer(serializers.Serializer):
    """
    Sérializer pour la vue ChangePasswordView.
    """
    old_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        min_length=6
    )

    def validate_new_password(self, value):
        """
        Validation du mot de passe avec les règles de Django.
        """
        validate_password(value)
        return value

