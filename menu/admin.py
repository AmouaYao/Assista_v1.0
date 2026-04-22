from django.contrib import admin
from .models import MenuItem, Commande, LigneCommande


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name']
    ordering = ['category', 'order']
    list_editable = ['is_active']
    
    def get_list_display(self, request):
        display = ['name', 'category', 'price', 'order']
        if request.user.is_superuser:
            display.append('is_active')
        return display

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('reference', 'session', 'table', 'client_telephone', 'total', 'pourboire', 'total_avec_pourboire', 'statut', 'date_creation', 'whatsapp_envoye')
    list_filter = ('statut', 'date_creation', 'whatsapp_envoye')
    search_fields = ('table', 'client_telephone')
    ordering = ['-date_creation']
    readonly_fields = ('date_creation',)
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('table', 'client_telephone', 'total', 'pourboire', 'total_avec_pourboire', 'statut')
        }),
        ('Détails', {
            'fields': ('notes', 'date_creation', 'whatsapp_envoye')
        }),
    )

@admin.register(LigneCommande)
class LigneCommandeAdmin(admin.ModelAdmin):
    list_display = ('session', 'menu_item', 'quantite', 'prix_unitaire', 'sous_total')
    list_filter = ('commande__statut', 'menu_item__category')
    search_fields = ('commande__table', 'menu_item__name')
    ordering = ['-commande__date_creation']
    
    def sous_total(self, obj):
        return obj.sous_total()
    sous_total.short_description = 'Sous-total'



