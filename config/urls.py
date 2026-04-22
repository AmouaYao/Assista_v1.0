from django.urls import path
from . import views

urlpatterns = [
    path('sauvegarder-commande/', views.sauvegarder_commande, name='sauvegarder_commande'),
    path('generate-wave-url/', views.generate_wave_payment_url, name='generate_wave_payment_url'),
]
