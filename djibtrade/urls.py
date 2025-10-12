from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
import datetime

# 🔥 HEALTH CHECK SIMPLIFIÉ (Garanti de fonctionner)
def health_check(request):
    return JsonResponse({
        "status": "healthy",
        "service": "Djibtrade API", 
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0",
        "message": "Backend is running smoothly"
    })

def health_check_simple(request):
    return JsonResponse({
        "status": "healthy", 
        "timestamp": datetime.datetime.now().isoformat()
    })

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('health/simple/', health_check_simple, name='health_check_simple'),
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/annonces/', include('products.urls')),
    path('api/', include('subscriptions.urls')),
    path('api/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)