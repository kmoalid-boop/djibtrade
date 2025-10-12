import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from .models import User

# Configuration du logger
logger = logging.getLogger(__name__)

# 🔥 NOUVEAU : Fonction pour obtenir l'URL du frontend dynamiquement
def get_frontend_url():
    """Retourne l'URL du frontend selon l'environnement"""
    if settings.DEBUG:
        return "http://localhost:5173"  # Développement
    else:
        # En production, utilise FRONTEND_URL ou l'URL par défaut
        return getattr(settings, 'FRONTEND_URL', 'https://djibtrade.netlify.app')

# 🔹 Signal : Token de réinitialisation de mot de passe (VERSION CORRIGÉE)
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Envoie un email HTML professionnel avec un lien cliquable pour la réinitialisation.
    """
    try:
        # 🔥 CORRECTION : URL dynamique
        frontend_url = get_frontend_url()
        reset_url = f"{frontend_url}/reset-password?token={reset_password_token.key}"
        
        # Context pour le template
        context = {
            'reset_url': reset_url,
            'user': reset_password_token.user,
            'token': reset_password_token.key
        }
        
        # Rendre le template HTML
        html_content = render_to_string('email/password_reset.html', context)
        
        # Version texte pour les clients email qui ne supportent pas HTML
        text_content = f"""
        Réinitialisation de mot de passe DjibTrade
        
        Bonjour,
        
        Vous avez demandé la réinitialisation de votre mot de passe DjibTrade.
        
        Pour réinitialiser votre mot de passe, cliquez sur le lien suivant :
        {reset_url}
        
        Si le lien ne fonctionne pas, copiez-collez cette URL dans votre navigateur.
        
        Si vous n'avez pas demandé cette réinitialisation, veuillez ignorer cet email.
        
        Ce lien expirera dans 24 heures pour des raisons de sécurité.
        
        Cordialement,
        L'équipe DjibTrade
        """
        
        # Créer l'email avec les deux versions (texte et HTML)
        msg = EmailMultiAlternatives(
            subject="Réinitialisation de votre mot de passe DjibTrade",
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[reset_password_token.user.email]
        )
        msg.attach_alternative(html_content, "text/html")
        
        # Envoyer l'email
        msg.send()
        
        logger.info(f"📩 Email de réinitialisation envoyé à {reset_password_token.user.email}")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'envoi de l'email de reset : {e}")

# 🔹 Signal : Envoi d'email de bienvenue après inscription (VERSION CORRIGÉE)
@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Envoie un email de bienvenue HTML lorsqu'un nouvel utilisateur est créé.
    """
    if created:
        logger.info(f"🎉 Nouvel utilisateur créé : {instance.email} ({instance.role})")

        try:
            # 🔥 CORRECTION : URL dynamique
            frontend_url = get_frontend_url()
            
            # Context pour le template de bienvenue
            context = {
                'user': instance,
                'company_name': instance.company_name,
                'login_url': f"{frontend_url}/login"
            }
            
            # Rendre le template HTML
            html_content = render_to_string('email/welcome.html', context)
            
            # Version texte
            text_content = f"""
            Bonjour {instance.company_name},

            Bienvenue sur Djibtrade ! Nous sommes ravis de vous compter parmi nous.
            
            Vous pouvez maintenant vous connecter et publier vos annonces :
            {frontend_url}/login
            
            À très bientôt,
            L'équipe Djibtrade
            """
            
            # Créer l'email
            msg = EmailMultiAlternatives(
                subject="Bienvenue sur Djibtrade 🎉",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[instance.email]
            )
            msg.attach_alternative(html_content, "text/html")
            
            # Envoyer l'email
            msg.send()
            
            logger.info(f"📩 Email de bienvenue envoyé à {instance.email}")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'envoi de l'email de bienvenue : {e}")