# Generated by Django 5.1.2 on 2024-10-20 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0002_alter_goal_goal_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='user',
        ),
    ]
