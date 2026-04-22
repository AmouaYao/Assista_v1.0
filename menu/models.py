from django.db import models
from django.utils import timezone

class MenuItem(models.Model):
    CATEGORIES = [
        ('boissons', 'Boissons'),
        ('snacks', 'Snacks'),
        ('plats', 'Plats'),
        ('desserts', 'Desserts'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    emoji = models.CharField(max_length=10, blank=True, null=True)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        ordering = ['category', 'order']
    
    def __str__(self):
        return f"{self.name} - {self.price} FCFA"

class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('preparation', 'En préparation'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]
    
    reference = models.CharField(max_length=20, unique=True, blank=True)
    session = models.CharField(max_length=20, unique=True, blank=True)
    table = models.CharField(max_length=10)
    client_telephone = models.CharField(max_length=20)
    total = models.IntegerField()
    pourboire = models.IntegerField(default=70)
    total_avec_pourboire = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_creation = models.DateTimeField(default=timezone.now)
    whatsapp_envoye = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.reference}"
    
    def save(self, *args, **kwargs):
        if not self.reference:
            # Générer une référence unique: CMD + année mois jour + ID
            import random
            import string
            today = timezone.now().strftime("%y%m%d")
            random_suffix = ''.join(random.choices(string.digits, k=4))
            self.reference = f"CMD{today}{random_suffix}"
        
        if not self.session:
            # Générer une session unique: S + 6 chiffres aléatoires
            import random
            self.session = f"S{''.join(random.choices(string.digits, k=6))}"
        
        # Calculer automatiquement le total avec pourboire
        self.total_avec_pourboire = self.total + self.pourboire
        
        super().save(*args, **kwargs)

class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    session = models.CharField(max_length=20)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire = models.IntegerField()
    
    def sous_total(self):
        return self.quantite * self.prix_unitaire
    
    def save(self, *args, **kwargs):
        if not self.session and self.commande:
            # Hériter la session de la commande
            self.session = self.commande.session
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.quantite}x {self.menu_item.name} ({self.session})"
