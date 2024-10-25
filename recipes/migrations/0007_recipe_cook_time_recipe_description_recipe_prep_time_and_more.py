# Generated by Django 5.1.2 on 2024-10-23 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_remove_recipe_total_calories_recipeingredient_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='cook_time',
            field=models.PositiveIntegerField(default=10, help_text='Cooking time in minutes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='prep_time',
            field=models.PositiveIntegerField(default=15, help_text='Preparation time in minutes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='servings',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='recipe',
            name='steps',
            field=models.TextField(default='cook'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='type',
            field=models.CharField(choices=[('appetizer', 'Appetizer'), ('main_course', 'Main Course'), ('dessert', 'Dessert'), ('vegan', 'Vegan'), ('vegetarian', 'Vegetarian'), ('gluten_free', 'Gluten Free'), ('paleo', 'Paleo'), ('keto', 'Keto'), ('low_carb', 'Low Carb')], default='main_course', max_length=50),
        ),
    ]
