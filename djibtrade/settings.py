import os
import re
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# ==================== CONFIGURATION DE BASE ====================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')  # Charge les variables d'environnement

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'

# ==================== HÔTES AUTORISÉS ====================
# Autorise tous les sous-domaines Ngrok en développement
if DEBUG:
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        '.ngrok-free.app',
        '.ngrok.io',
        # Ajoutez vos IPs locales si nécessaire
        '192.168.5.1',
        '192.168.231.1',
        '10.147.106.224',
    ]
else:
    ALLOWED_HOSTS = ['djibtrade.com']

# ==================== APPLICATIONS ====================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_rest_passwordreset',
    'accounts.apps.AccountsConfig',
    'products.apps.ProductsConfig',
    'subscriptions.apps.SubscriptionsConfig',
    'notifications.apps.NotificationsConfig',
]

# ==================== MIDDLEWARE ====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# ==================== TEMPLATES & URLs ====================
ROOT_URLCONF = 'djibtrade.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djibtrade.wsgi.application'

# ==================== BASE DE DONNÉES ====================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==================== AUTHENTIFICATION ====================
AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==================== INTERNATIONALISATION ====================
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Djibouti'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ==================== FICHIERS STATIQUES ====================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ==================== CORS ====================
if DEBUG:
    # En développement, autorisez tous les domaines Ngrok
    CORS_ALLOW_ALL_ORIGINS = False  # Désactivé pour utiliser les regex
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^http://localhost:\d+$",
        r"^http://192\.168\.\d+\.\d+:\d+$",
        r"^http://10\.\d+\.\d+\.\d+:\d+$",
        r"^https://[a-z0-9-]+\.ngrok-free\.app$",
        r"^https://[a-z0-9-]+\.ngrok\.io$",
    ]
    # Ajoutez aussi les origines spécifiques que vous voulez
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",  # Port de Vite
    ]
    
    # CONFIGURATION CSRF AJOUTÉE ICI
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:5173",
        "https://*.ngrok-free.app",
        "https://*.ngrok.io",
    ]
    
    # Pour le débogage
    print("=" * 50)
    print("MODE DÉVELOPPEMENT ACTIVÉ")
    print("Hôtes autorisés:", ALLOWED_HOSTS)
    print("Origines CORS autorisées:", CORS_ALLOWED_ORIGINS)
    print("Origines CSRF autorisées:", CSRF_TRUSTED_ORIGINS)
    print("=" * 50)
else:
    # En production, soyez plus restrictif
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [
        "https://djibtrade.com",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "https://djibtrade.com",
    ]

# ==================== REST FRAMEWORK ====================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# ==================== JWT ====================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ==================== EMAIL ====================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == 'True'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# ==================== SÉCURITÉ PRODUCTION ====================
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_PRELOAD = True