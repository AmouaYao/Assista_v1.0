import json
from django.conf import settings
from django.shortcuts import render
from .models import MenuItem
from config.models import Etablissement

def splash_screen(request):
    return render(request, 'splash_screen.html')

def MenuOrderView(request):
    menu_items = MenuItem.objects.filter(is_active=True)
    
    # Organiser les items par catégorie pour le template
    categories = {
        'boissons': [],
        'snacks': [],
        'plats': [],
        'desserts': []
    }
    
    for item in menu_items:
        categories[item.category].append({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': item.price,
            'emoji': item.emoji,
            'image': item.image.url if item.image else None
        })
    
    menu_items_js = {str(item.id): {
        'name': item.name,
        'price': item.price,
        'emoji': item.emoji,
        'image': item.image.url if item.image else None
    } for item in menu_items}
    
    # Récupérer les paramètres de l'établissement
    etablissement = Etablissement.objects.first()
    frais_application_actives = etablissement.frais_application_actives if etablissement else True
    montant_frais_application = etablissement.montant_frais_application if etablissement else 70
    
    return render(request, 'menu_order.html', {
        'WAVE_URL': settings.WAVE_URL,
        'menu_categories': categories,
        'menu_items_js': json.dumps(menu_items_js),
        'frais_application_actives': frais_application_actives,
        'montant_frais_application': montant_frais_application
    })
