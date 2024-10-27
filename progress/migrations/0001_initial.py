# Generated by Django 5.1.2 on 2024-10-26 07:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goals', '0005_goal_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress_date', models.DateField()),
                ('value', models.FloatField()),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to='goals.goal')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='progresses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
