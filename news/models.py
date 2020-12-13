from datetime import datetime
from django.db import models


class Player(models.Model):
	name = models.CharField(max_length=200)
	current_projection = models.IntegerField()

class Article(models.Model):
	url = models.CharField(max_length=400)
	image_path = models.CharField(max_length=400)
	title = models.CharField(max_length=400)
	source = models.CharField(max_length=400)
	date = models.CharField(max_length=200)