from django.db import models
from django.contrib.auth.models import User


class Progress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='progress',
        default=1
    )
    goal = models.ForeignKey(
        'goals.Goal',  
        on_delete=models.CASCADE,
        related_name='progress'
    )
    progress_date = models.DateField()
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.goal.title} ({self.goal.goal_type}) Progress on {self.progress_date}: {self.value}"
