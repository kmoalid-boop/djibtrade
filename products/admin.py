from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'owner', 
        'unit_price', 
        'currency', 
        'stock', 
        'total_price', 
        'category', 
        'city',
        'contact_method',
        'views',
        'created_at'
    )
    list_filter = (
        'category',
        'currency',
        'contact_method',
        'city',
        'created_at'
    )
    search_fields = (
        'title',
        'description',
        'owner__username',
        'owner__email'
    )
    readonly_fields = (
        'total_price',
        'whatsapp_link',
        'views',
        'created_at'
    )
    fieldsets = (
        ('Informations principales', {
            'fields': (
                'title',
                'description',
                'owner',
                'category',
                'city'
            )
        }),
        ('Prix et stock', {
            'fields': (
                'unit_price',
                'currency',
                'stock',
                'total_price'
            )
        }),
        ('Contact', {
            'fields': (
                'contact_method',
                'whatsapp_contact',
                'phone_contact',
                'whatsapp_link'
            )
        }),
        ('Médias et statistiques', {
            'fields': (
                'image',
                'views',
                'created_at'
            )
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    search_fields = ('name',)
    
    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Nombre de produits'