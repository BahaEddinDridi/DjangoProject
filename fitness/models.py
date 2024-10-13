# fitness/models.py

from django.db import models

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
    muscles_targeted = models.CharField(max_length=100)

    def __str__(self):
        return self.name
