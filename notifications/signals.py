from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from products.models import Product
from .models import Notification, NotificationPreferences

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_notification_preferences(sender, instance, created, **kwargs):
    if created:
        NotificationPreferences.objects.create(user=instance)

@receiver(post_save, sender=Product)
def notify_product_creation(sender, instance, created, **kwargs):
    if created:
        # Créer une notification pour l'utilisateur qui a créé le produit
        Notification.objects.create(
            user=instance.owner,
            title="Annonce publiée",
            message=f"Votre annonce '{instance.title}' a été publiée avec succès.",
            notification_type='success',
            related_product=instance
        )
        
        # Notifier tous les autres utilisateurs
        users_to_notify = User.objects.exclude(id=instance.owner.id)
        
        for user in users_to_notify:
            # Vérifier si l'utilisateur veut recevoir des notifications de nouveaux produits
            preferences, created = NotificationPreferences.objects.get_or_create(user=user)
            
            if preferences.product_updates:
                Notification.objects.create(
                    user=user,
                    title="Nouvelle annonce disponible",
                    message=f"Une nouvelle annonce '{instance.title}' a été publiée. Découvrez-la dès maintenant!",
                    notification_type='info',
                    related_product=instance
                )