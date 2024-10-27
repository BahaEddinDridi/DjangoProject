from django import forms
from .models import EvenementSportif

class EvenementSportifForm(forms.ModelForm):
    class Meta:
        model = EvenementSportif
        fields = ['titre', 'description', 'date_debut', 'date_fin','lieu','participants']