import logging
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from .models import User

# Configuration du logger
logger = logging.getLogger(__name__)

# 🔹 Signal : Token de réinitialisation de mot de passe
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Envoie un email contenant le token de réinitialisation de mot de passe.
    """
    email_plaintext_message = f"Voici votre token de réinitialisation : {reset_password_token.key}"

    try:
        send_mail(
            subject="Réinitialisation de mot de passe",
            message=email_plaintext_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reset_password_token.user.email],
            fail_silently=False
        )
        logger.info(f"📩 Email de réinitialisation envoyé à {reset_password_token.user.email}")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'envoi de l'email de reset : {e}")

# 🔹 Signal : Envoi d'email de bienvenue après inscription
@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Envoie un email de bienvenue lorsqu'un nouvel utilisateur est créé.
    """
    if created:
        logger.info(f"🎉 Nouvel utilisateur créé : {instance.email} ({instance.role})")

        try:
            send_mail(
                subject="Bienvenue sur Djibtrade 🎉",
                message=(
                    f"Bonjour {instance.company_name},\n\n"
                    "Bienvenue sur Djibtrade ! Nous sommes ravis de vous compter parmi nous.\n"
                    "Vous pouvez maintenant vous connecter et publier vos annonces.\n\n"
                    "À très bientôt,\nL'équipe Djibtrade"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=True
            )
            logger.info(f"📩 Email de bienvenue envoyé à {instance.email}")
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'envoi de l'email de bienvenue : {e}")
