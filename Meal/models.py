from django.db import models

class Meal(models.Model):
    name = models.CharField(max_length=100)
    calories = models.FloatField()
    protein = models.FloatField()  
    carbs = models.FloatField()  
    fat = models.FloatField() 
