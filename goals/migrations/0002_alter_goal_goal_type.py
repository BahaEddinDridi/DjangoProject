# Generated by Django 5.1.2 on 2024-10-20 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='goal_type',
            field=models.CharField(choices=[('Perte de poids', 'Perte de poids'), ('Gain musculaire', 'Gain musculaire'), ('Amélioration de la performance', 'Amélioration de la performance')], default='Perte de poids', max_length=100),
        ),
    ]