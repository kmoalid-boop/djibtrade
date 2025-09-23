from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/annonces/', include('products.urls')),
    path('api/', include('subscriptions.urls')),
    path('api/', include('notifications.urls')),  # Ajoutez cette ligne
]

# ✅ Configuration pour servir les médias
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)