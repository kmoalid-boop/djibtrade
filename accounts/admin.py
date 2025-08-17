from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Configuration de l’affichage du modèle User dans l’admin Django.
    """
    list_display = ('company_name', 'email', 'phone', 'role', 'is_premium', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_premium', 'is_staff', 'date_joined')
    search_fields = ('company_name', 'email', 'phone')
    readonly_fields = ('date_joined',)
    ordering = ('-date_joined',)
