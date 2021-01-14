import datetime
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Player, Article
from .predictions import predictions
from .names import names
from .serializers import PlayerSerializer, ArticleSerializer
from .webscrape import get_fantasy, get_yahoo, get_espn, search_player
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
import datetime

# Main View
index = never_cache(TemplateView.as_view(template_name="index.html"))


@api_view(['GET'])
def api_home(request):
	return HttpResponse('Home')

@api_view(['GET'])
def api_articles(request):
	duplicates = list(Article.objects.all())
	for article in duplicates[:]:
		if len(Article.objects.filter(title=article.title)) > 1:
			print(article)
			article.delete()

	serializer = ArticleSerializer(list(Article.objects.filter(source="fantasy")), many=True)
	return Response(serializer.data)

@api_view(['GET'])
def api_players(request):
	duplicates = list(Player.objects.all())
	for player in duplicates[:]:
		if len(Player.objects.filter(name=player.name)) > 1:
			player.delete()
	# print(Player.objects.filter(name="Christian McCaffrey"))
	serializer = PlayerSerializer(list(Player.objects.all()), many=True)
	return Response(serializer.data)

@api_view(['POST', 'GET'])
def api_predict(request):
	name = request.data['playerName']
	print(name)
	response = Player.objects.all()
	try:
		response = Player.objects.get(name=name)
	except Exception as e:
		result = search_player(name)
		prediction = predictions(result[0], result[1], result[2])
		player = Player(name=name, current_projection=int(round(prediction[0])), position=result[4], image_path=result[3], team=None)
		player.save()
		response = player

	serializer = PlayerSerializer(response)
	return Response(serializer.data)

@api_view(['POST', 'GET'])
def api_filter(request):
	search = request.data['query'].lower()
	print(search)
	if 'yahoo' == search or 'espn' == search or 'fantasy pros' == search:
		serializer = ArticleSerializer(list(Article.objects.filter(source=search)), many=True)
		return Response(serializer.data)

	filtered_news = []
	for article in Article.objects.all():
		if article.date in search or search in article.title:
			filtered_news.append(article)
	serializer = ArticleSerializer(filtered_news, many=True)

	return Response(serializer.data)

# updates the database every week
def update_database():
	projections = []
	Player.objects.all().delete()
	for name in names.keys():
		try:
			result = search_player(name)
			prediction = predictions(result[0], result[1], result[2])
			projections.append([name, prediction])
		except:
			continue 

	def by_projection(item):
		return item[1]

	projections.sort(key=by_projection)
	for i in projections[::-1]:
		if i[1] > 0:
			result = search_player(i[0])
			player = Player(name=i[0], current_projection=int(round(i[1][0])), position=names[i[0]][1][:2], image_path=result[3], team=names[i[0]][0])
			player.save()
		else:
			break

# the following functions determine what gets rendered on different pages of the website.

def update_page(request):

	Article.objects.all().delete()
	fantasy_pros = get_fantasy()

	update_database()

	week = datetime.date.today()
	Article.objects.all().delete()
	if len(Article.objects.all()) > 90:
		for article in list(Article.objects.all())[72:]:
			article.delete()

	my_date = datetime.date.today() 
	year, week_num, day_of_week = my_date.isocalendar()

	for story in get_yahoo():
		yahoo_stories = [article.title for article in list(Article.objects.filter(source="yahoo"))]
		if story[0] not in yahoo_stories:
			article = Article(title=story[0], url=story[1], image_path='static', source="yahoo", date=week)
			article.save()

	for story in get_espn():
		espn_stories = [article.title for article in list(Article.objects.filter(source="espn"))]
		if story[0] not in espn_stories:
			article = Article(title=story[0], url=story[1], image_path='static', source="espn", date=week)
			article.save()

	for story in fantasy_pros.keys():
		fantasy_stories = [article.title for article in list(Article.objects.filter(source="fantasy"))]
		if story[0] not in fantasy_stories:
			article = Article(title=story, url=fantasy_pros[story][0], image_path=fantasy_pros[story][1], source="fantasy", date=week)
			article.save()

	print(Player.objects.all())
	return HttpResponse('<h1>Database updated</h1>')

