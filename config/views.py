from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
import hashlib
import time
from menu.models import MenuItem, Commande, LigneCommande
from .models import Etablissement

@csrf_exempt
def sauvegarder_commande(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Récupérer les paramètres de l'établissement
            etablissement = Etablissement.objects.first()
            frais_actives = etablissement.frais_application_actives if etablissement else True
            montant_frais = etablissement.montant_frais_application if etablissement else 70
            
            # Calculer les frais d'application
            nombre_articles = sum(item['quantite'] for item in data.get('items', []))
            pourboire_total = nombre_articles * montant_frais if frais_actives else 0
            
            # Créer la commande 
            commande = Commande.objects.create(
                table=data.get('table'),
                client_telephone=data.get('client_telephone'),
                total=data.get('total'),
                pourboire=pourboire_total,  # Pourboire calculé dynamiquement
                notes=data.get('notes', ''),
                statut='en_attente'
            )
            
            # Créer les lignes de commande
            for item_data in data.get('items', []):
                menu_item = MenuItem.objects.get(id=item_data['id'])
                LigneCommande.objects.create(
                    commande=commande,
                    menu_item=menu_item,
                    quantite=item_data['quantite'],
                    prix_unitaire=menu_item.price
                )
            
            return JsonResponse({
                'success': True,
                'commande_id': commande.id,
                'reference': commande.reference,
                'session': commande.session,
                'total': commande.total,
                'pourboire': commande.pourboire,
                'total_avec_pourboire': commande.total_avec_pourboire,
                'message': 'Commande sauvegardée avec succès'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
@require_http_methods(["POST"])
def generate_wave_payment_url(request):
    """
    Génère une URL de paiement Wave sécurisée
    """
    try:
        from django.conf import settings
        
        # Récupérer les données
        data = json.loads(request.body)
        amount = data.get('amount', 0)
        
        # Validation du montant
        if amount <= 0:
            return JsonResponse({
                'success': False,
                'error': 'Montant invalide'
            }, status=400)
        
        # Créer un token unique pour cette transaction
        timestamp = str(int(time.time()))
        token_data = f"{amount}_{timestamp}_{settings.WAVE_TOKEN}"
        transaction_token = hashlib.sha256(token_data.encode()).hexdigest()[:16]
        
        # Construire les URLs Wave (format simple comme dans l'app)
        app_wave_url = f"https://pay.wave.com/m/M_ci_-5o8YqgPD6iB/c/ci/?amount={amount}"
        web_wave_url = f"https://pay.wave.com/m/M_ci_-5o8YqgPD6iB/c/ci/?amount={amount}"
        wave_url = web_wave_url  # URL principale
        
        # Journaliser la transaction pour audit
        print(f"Wave payment URL generated: amount={amount}, token={transaction_token}")
        print(f"Complete Wave URL: {wave_url}")
        
        return JsonResponse({
            'success': True,
            'wave_url': wave_url,
            'app_wave_url': app_wave_url,
            'web_wave_url': web_wave_url,
            'amount': amount,
            'transaction_token': transaction_token,
            'debug_url': wave_url  # Pour débogage
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erreur lors de la génération: {str(e)}'
        }, status=500)
