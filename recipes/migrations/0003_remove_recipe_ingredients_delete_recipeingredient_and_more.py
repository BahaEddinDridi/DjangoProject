# Generated by Django 5.1.2 on 2024-10-20 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_rename_calories_ingredient_calories_per_unit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.DeleteModel(
            name='RecipeIngredient',
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.JSONField(default=list),
        ),
    ]
