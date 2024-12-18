from django.db import models
from django.contrib.auth.models import User 

class Goal(models.Model):
    class GoalType(models.TextChoices):
        WEIGHT_LOSS = 'Perte de poids', 'Perte de poids'
        MUSCLE_GAIN = 'Gain musculaire', 'Gain musculaire'
        PERFORMANCE_IMPROVEMENT = 'Amélioration de la performance', 'Amélioration de la performance'

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='goals',
        default=1
    )
    title = models.CharField(max_length=255, default="Untitled Goal")  
    goal_type = models.CharField(
        max_length=100,
        choices=GoalType.choices,
        default=GoalType.WEIGHT_LOSS
    )
    target_value = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.goal_type} (Cible: {self.target_value})"
