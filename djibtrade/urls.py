from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.db import connection
from django.db.utils import OperationalError
import datetime
import platform
import psutil
import os

# 🔥 HEALTH CHECK AVANCÉ - Version Professionnelle
def health_check(request):
    """
    Endpoint de santé complet pour monitoring avancé
    Retourne l'état de santé de l'application et des services
    """
    # Temps de démarrage de l'application
    start_time = datetime.datetime.now()
    
    # Vérifications des services
    checks = {
        "database": check_database(),
        "storage": check_storage(),
        "memory": check_memory(),
        "environment": check_environment()
    }
    
    # Déterminer le statut global
    all_healthy = all(check["status"] == "healthy" for check in checks.values())
    overall_status = "healthy" if all_healthy else "degraded"
    
    # Temps de réponse
    response_time = (datetime.datetime.now() - start_time).total_seconds() * 1000
    
    return JsonResponse({
        # 🔍 Statut général
        "status": overall_status,
        "timestamp": datetime.datetime.now().isoformat(),
        "response_time_ms": round(response_time, 2),
        
        # 🏷️ Informations service
        "service": "Djibtrade API",
        "version": "1.0.0",
        "environment": "production" if not settings.DEBUG else "development",
        
        # 📊 Métriques système
        "system": {
            "python_version": platform.python_version(),
            "django_version": settings.VERSION,
            "server_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "timezone": str(settings.TIME_ZONE),
        },
        
        # 🔧 Vérifications détaillées
        "checks": checks,
        
        # 📈 Statistiques (si disponibles)
        "stats": get_basic_stats() if overall_status == "healthy" else {},
        
        # 🔗 Endpoints disponibles
        "endpoints": {
            "admin": f"{request.build_absolute_uri('/admin/')}",
            "api_docs": f"{request.build_absolute_uri('/api/')}",
            "products": f"{request.build_absolute_uri('/api/annonces/products/')}",
            "categories": f"{request.build_absolute_uri('/api/annonces/categories/')}",
        }
    })

# 🔧 FONCTIONS DE VÉRIFICATION

def check_database():
    """Vérifie la connexion à la base de données"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return {
            "status": "healthy",
            "details": "Database connection successful",
            "database": connection.vendor,
            "response_time": "fast"
        }
    except OperationalError as e:
        return {
            "status": "unhealthy", 
            "details": f"Database error: {str(e)}",
            "database": connection.vendor,
            "response_time": "timeout"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "details": f"Unexpected database error: {str(e)}",
            "database": "unknown",
            "response_time": "error"
        }

def check_storage():
    """Vérifie l'espace disque et le stockage"""
    try:
        # Vérification espace disque
        disk_usage = psutil.disk_usage('/')
        disk_free_gb = round(disk_usage.free / (1024**3), 1)
        disk_total_gb = round(disk_usage.total / (1024**3), 1)
        disk_percent_free = round((disk_usage.free / disk_usage.total) * 100, 1)
        
        # Vérification mémoire
        memory = psutil.virtual_memory()
        memory_percent = round(memory.percent, 1)
        
        return {
            "status": "healthy" if disk_percent_free > 10 and memory_percent < 90 else "warning",
            "details": "Storage systems operational",
            "disk": {
                "free_gb": disk_free_gb,
                "total_gb": disk_total_gb,
                "percent_free": disk_percent_free
            },
            "memory": {
                "percent_used": memory_percent,
                "available_gb": round(memory.available / (1024**3), 1)
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "details": f"Storage check failed: {str(e)}",
            "disk": "unknown",
            "memory": "unknown"
        }

def check_memory():
    """Vérifie l'utilisation mémoire de l'application"""
    try:
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        memory_mb = round(memory_info.rss / (1024**2), 1)
        
        return {
            "status": "healthy" if memory_mb < 500 else "warning",  # Moins de 500MB = OK
            "details": f"Application memory usage: {memory_mb}MB",
            "memory_used_mb": memory_mb,
            "threshold_mb": 500
        }
    except Exception as e:
        return {
            "status": "unknown",
            "details": f"Memory check failed: {str(e)}",
            "memory_used_mb": "unknown"
        }

def check_environment():
    """Vérifie les variables d'environnement critiques"""
    required_env_vars = [
        'SECRET_KEY',
        'DATABASE_URL',
        'CLOUDINARY_CLOUD_NAME',
        'CLOUDINARY_API_KEY', 
        'CLOUDINARY_API_SECRET'
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        return {
            "status": "unhealthy",
            "details": f"Missing environment variables: {', '.join(missing_vars)}",
            "missing_variables": missing_vars
        }
    else:
        return {
            "status": "healthy",
            "details": "All required environment variables are set",
            "missing_variables": []
        }

def get_basic_stats():
    """Récupère des statistiques basiques (seulement si tout est healthy)"""
    try:
        from django.contrib.auth import get_user_model
        from products.models import Product, Category
        
        User = get_user_model()
        
        return {
            "users_count": User.objects.count(),
            "products_count": Product.objects.count(),
            "categories_count": Category.objects.count(),
            "active_products": Product.objects.filter(stock__gt=0).count()
        }
    except Exception:
        # En cas d'erreur, on retourne des stats vides (mieux que de faire planter le health check)
        return {
            "users_count": "unknown",
            "products_count": "unknown", 
            "categories_count": "unknown",
            "active_products": "unknown"
        }

# 🔥 HEALTH CHECK SIMPLE (Version légère pour Render)
def health_check_simple(request):
    """
    Version simplifiée du health check pour les vérifications rapides
    Utilisé par Render pour les health checks automatiques
    """
    try:
        # Vérification basique de la base de données
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            "status": "healthy",
            "timestamp": datetime.datetime.now().isoformat(),
            "service": "Djibtrade API"
        })
    except Exception as e:
        return JsonResponse({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.datetime.now().isoformat()
        }, status=500)

urlpatterns = [
    # 🔥 Health Check Avancé (pour le monitoring détaillé)
    path('health/', health_check, name='health_check'),
    
    # 🔥 Health Check Simple (pour Render et vérifications rapides)
    path('health/simple/', health_check_simple, name='health_check_simple'),
    
    # Routes existantes
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/annonces/', include('products.urls')),
    path('api/', include('subscriptions.urls')),
    path('api/', include('notifications.urls')),
]

# ✅ Configuration pour servir les médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)