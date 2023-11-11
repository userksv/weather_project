from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=128, unique=True)                # Location name
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)         # User who added location
    lattitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f'{self.name} - {self.user_id}'
