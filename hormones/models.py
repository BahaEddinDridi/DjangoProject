from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class HormoneLevel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hormone_name = models.CharField(max_length=100) 
    level = models.FloatField()
    unit = models.CharField(max_length=20)
    date_measured = models.DateField()

    def __str__(self):
        return f"{self.hormone_name} ({self.level} {self.unit})"
    


class HormoneRecommendation(models.Model):
    hormone_level = models.ForeignKey(HormoneLevel, on_delete=models.CASCADE)
    recommendation = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for {self.hormone_level.hormone_name}"    

