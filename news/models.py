from django.db import models

# Create your models here.
class Player(models.Model):
	name = models.CharField(max_length=200)
	current_projection = models.IntegerField()