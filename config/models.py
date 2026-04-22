from django.db import models

class Etablissement(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    tiktok = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to='logos/')
    frais_application_actives = models.BooleanField(default=True, verbose_name="Activer les frais d'application")
    montant_frais_application = models.IntegerField(default=70, verbose_name="Montant des frais d'application (FCFA)")
    
    def __str__(self):
        return self.nom
