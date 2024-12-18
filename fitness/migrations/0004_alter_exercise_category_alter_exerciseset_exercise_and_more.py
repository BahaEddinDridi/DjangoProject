# Generated by Django 5.1.2 on 2024-10-23 15:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0003_alter_exerciseset_sets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='category',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='exerciseset',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_sets', to='fitness.exercise'),
        ),
        migrations.AlterField(
            model_name='exerciseset',
            name='sets',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='exerciseset',
            name='training_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_sets', to='fitness.trainingplan'),
        ),
    ]
