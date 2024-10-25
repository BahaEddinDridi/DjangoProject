from django.contrib import admin
from .models import Meal, NutritionPlan

# Register your models here.

admin.site.register(Meal)
admin.site.register(NutritionPlan)
