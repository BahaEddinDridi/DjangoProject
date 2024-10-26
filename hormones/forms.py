from django import forms
from .models import HormoneLevel, HormoneRecommendation

class HormoneLevelForm(forms.ModelForm):
    class Meta:
        model = HormoneLevel
        fields = ['hormone_name', 'level', 'unit', 'date_measured']

class HormoneRecommendationForm(forms.ModelForm):
    class Meta:
        model = HormoneRecommendation
        fields = ['hormone_level', 'recommendation']