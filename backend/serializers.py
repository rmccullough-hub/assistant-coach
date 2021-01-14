from rest_framework import serializers
from .models import Player, Article

class ArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields ='__all__'

class PlayerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Player
		fields ='__all__'