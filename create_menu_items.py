import os
import django

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'order.settings')
django.setup()

from menu.models import MenuItem

# Supprimer les items existants
MenuItem.objects.all().delete()

# Créer les items de base
items_data = [
    {
        'name': 'Bissap glacé',
        'description': 'Hibiscus, gingembre, menthe fraîche',
        'price': 1500,
        'category': 'boissons',
        'emoji': '🌺',
        'order': 1
    },
    {
        'name': 'Gingembre maison',
        'description': 'Jus de gingembre frais pressé',
        'price': 1500,
        'category': 'boissons',
        'emoji': '🫚',
        'order': 2
    },
    {
        'name': 'Jus de fruit frais',
        'description': 'Ananas, mangue ou pastèque',
        'price': 2000,
        'category': 'boissons',
        'emoji': '🥭',
        'order': 3
    },
    {
        'name': 'Eau minérale',
        'description': '50cl — plate ou gazeuse',
        'price': 500,
        'category': 'boissons',
        'emoji': '💧',
        'order': 4
    },
    {
        'name': 'Café / Thé',
        'description': 'Espresso ou thé à la menthe',
        'price': 1000,
        'category': 'boissons',
        'emoji': '☕',
        'order': 5
    },
    {
        'name': 'Alloco au poulet',
        'description': 'Banane plantain frite, poulet rôti',
        'price': 3500,
        'category': 'snacks',
        'emoji': '🍗',
        'order': 6
    },
    {
        'name': 'Spring rolls',
        'description': 'Légumes frais, sauce soja sucrée',
        'price': 2500,
        'category': 'snacks',
        'emoji': '🥢',
        'order': 7
    },
    {
        'name': 'Avocat vinaigrette',
        'description': 'Avocat Abidjan, citron, huile olive',
        'price': 2000,
        'category': 'snacks',
        'emoji': '🥑',
        'order': 8
    },
    {
        'name': 'Plateau fromages',
        'description': 'Sélection 3 fromages, crackers',
        'price': 4500,
        'category': 'snacks',
        'emoji': '🧀',
        'order': 9
    },
    {
        'name': 'Poisson braisé',
        'description': 'Tilapia entier, attiéké, sauce fraîche',
        'price': 7500,
        'category': 'plats',
        'emoji': '🐟',
        'order': 10
    },
    {
        'name': 'Poulet yassa',
        'description': 'Poulet mariné citron-oignon, riz',
        'price': 6500,
        'category': 'plats',
        'emoji': '🍛',
        'order': 11
    },
    {
        'name': 'Salade niçoise',
        'description': 'Thon, œuf, olives, vinaigrette maison',
        'price': 5500,
        'category': 'plats',
        'emoji': '🥗',
        'order': 12
    },
    {
        'name': 'Burger du jardin',
        'description': 'Bœuf, fromage, légumes grillés',
        'price': 6000,
        'category': 'plats',
        'emoji': '🍔',
        'order': 13
    },
    {
        'name': 'Fondant chocolat',
        'description': 'Cœur coulant, glace vanille',
        'price': 3000,
        'category': 'desserts',
        'emoji': '🍫',
        'order': 14
    },
    {
        'name': 'Salade de fruits',
        'description': 'Fruits de saison, coulis passion',
        'price': 2500,
        'category': 'desserts',
        'emoji': '🍓',
        'order': 15
    },
    {
        'name': 'Crème caramel',
        'description': 'Caramel maison, éclats de noix',
        'price': 2500,
        'category': 'desserts',
        'emoji': '🍮',
        'order': 16
    }
]

# Créer les items
for item_data in items_data:
    MenuItem.objects.create(**item_data)

print(f"Créé {len(items_data)} items dans la base de données")
