# Generated by Django 5.1.2 on 2024-10-25 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0004_alter_exercise_category_alter_exerciseset_exercise_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exerciseset',
            name='repetitions',
            field=models.PositiveIntegerField(),
        ),
    ]
