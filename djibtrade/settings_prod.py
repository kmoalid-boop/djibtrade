import os
import dj_database_url
from .settings import *  # Importe ta configuration existante

# ==================== CONFIGURATION PRODUCTION RENDER ====================
DEBUG = False

# Sécurité - Render génère automatiquement SECRET_KEY
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key-change-me')

# Hosts autorisés pour Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS = [
        RENDER_EXTERNAL_HOSTNAME,
        'djibtrade.com', 
        'www.djibtrade.com',
        'djibtrade-backend.onrender.com'
    ]
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# ==================== MIDDLEWARE PRODUCTION ====================
# Insérer WhiteNoise après SecurityMiddleware
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# ==================== BASE DE DONNÉES RENDER ====================
# Render fournit DATABASE_URL automatiquement
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

# ==================== FICHIERS STATIQUES AVEC WHITENOISE ====================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==================== CORS POUR VERCEL + RENDER ====================
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://djibtrade.netlify.app",
    "http://localhost:3000",
    "http://localhost:5173",
]

CSRF_TRUSTED_ORIGINS = [
      "https://djibtrade.netlify.app",
      "https://djibtrade.onrender.com",
]

CORS_ALLOW_CREDENTIALS = True

# ==================== SÉCURITÉ RENFORCÉE ====================
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True

# ==================== EMAIL PRODUCTION ====================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@djibtrade.com')

print("=" * 60)
print("🚀 CONFIGURATION PRODUCTION DJIBTRADE CHARGÉE")
print("=" * 60)