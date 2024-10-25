from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()

    def __str__(self):
        return self.name

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    steps = models.TextField()
    prep_time = models.PositiveIntegerField(help_text="Preparation time in minutes")  
    cook_time = models.PositiveIntegerField(help_text="Cooking time in minutes") 
    servings = models.PositiveIntegerField(default=1)  
    type = models.CharField(max_length=50, choices=[
        ('appetizer', 'Appetizer'),
        ('main_course', 'Main Course'),
        ('dessert', 'Dessert'),
        ('vegan', 'Vegan'),
        ('vegetarian', 'Vegetarian'),
        ('gluten_free', 'Gluten Free'),
        ('paleo', 'Paleo'),
        ('keto', 'Keto'),
        ('low_carb', 'Low Carb'),
    ], default='main_course') 
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

    def total_calories(self):
        return sum(ri.quantity * ri.ingredient.calories for ri in self.recipeingredient_set.all())

    def total_protein(self):
        return sum(ri.quantity * ri.ingredient.protein for ri in self.recipeingredient_set.all())

    def total_carbs(self):
        return sum(ri.quantity * ri.ingredient.carbs for ri in self.recipeingredient_set.all())

    def total_fat(self):
        return sum(ri.quantity * ri.ingredient.fat for ri in self.recipeingredient_set.all())

class RecipeIngredient(models.Model):
    UNITS = [
        ('g', 'grams'),
        ('kg', 'kilograms'),
        ('ml', 'milliliters'),
        ('l', 'liters'),
        ('cup', 'cups'),
        ('tbsp', 'tablespoons'),
        ('tsp', 'teaspoons'),
    ]
    
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=10, choices=UNITS)

    def __str__(self):
        return f'{self.quantity} {self.unit} of {self.ingredient.name} in {self.recipe.name}'
