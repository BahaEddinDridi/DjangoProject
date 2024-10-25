from django import forms
from .models import Meal, NutritionPlan

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'calories', 'protein', 'carbs','fat']

class NutritionPlanForm(forms.ModelForm):
    class Meta:
        model = NutritionPlan
        fields = ['user', 'meals','total_calories']