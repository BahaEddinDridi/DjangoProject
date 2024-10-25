from django.db import models
from django.contrib.auth.models import User

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    muscles_targeted = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TrainingPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    exercises = models.ManyToManyField(Exercise, through='ExerciseSet')
    date_created = models.DateTimeField(auto_now_add=True)

class ExerciseSet(models.Model):
    training_plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='exercise_sets')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='exercise_sets')
    sets = models.PositiveIntegerField(default=0)
    repetitions = models.PositiveIntegerField()
    rest_time = models.DurationField()  

    def __str__(self):
        return f"{self.exercise.name} - {self.sets} sets, {self.repetitions} reps, {self.rest_time} rest"
