from django.db import models
from django.contrib.auth.models import User

class EvenementSportif(models.Model):
    organisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evenements_organises')
    titre = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    lieu = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='evenements_participes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - Organisé par {self.organisateur.username}"
