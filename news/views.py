from django.shortcuts import render, redirect
from django.http import HttpResponse

from .webscrape import get_fantasy, get_yahoo, get_espn, search_player
from .forms import FilterForm, PredictionForm
from .predictions import predictions 
from .names import names
from .models import Player, Article
import datetime


# the following functions determine what gets rendered on different pages of the website.

def update_page(request):
	fantasy_pros = get_fantasy()
	# yahoo = get_yahoo()
	# espn = get_espn()

	Article.objects.all().delete()
	if len(Article.objects.all()) < 90:
		for story in get_yahoo():
			article = Article(title=story[0], url=story[1], image_path='static', source="yahoo")
			article.save()

		for story in get_espn():
			article = Article(title=story[0], url=story[1], image_path='static', source="espn")
			article.save()

		for story in fantasy_pros.keys():
			article = Article(title=story, url=fantasy_pros[story][0], image_path=fantasy_pros[story][1], source="fantasy" )
			article.save()

	return HttpResponse('<h1>Database updated</h1>')


# the home page contains news articles webscraped from several fantasy football websites and a form to filter these results.
def news_page(request, id=1):
	context = {}

	print(id)
	news_list = [[article.title, article.url, article.image_path] for article in list(Article.objects.filter(source='fantasy'))]

	yahoo_news = [[article.title, article.url] for article in list(Article.objects.filter(source='yahoo'))]

	espn_news = [[article.title, article.url] for article in list(Article.objects.filter(source='espn'))]

	form = FilterForm()
	
	num_of_articles = len(news_list) + len(yahoo_news) + len(espn_news)

	fantasy_ind = len(news_list)

	yahoo_ind = len(yahoo_news) 

	espn_ind = len(espn_news)

	print(len(Article.objects.all()))
	print(news_list)
	if id == 1 and num_of_articles <= 18:
		news_list = news_list[0:9]
		yahoo_news = yahoo_news[0:6]
		espn_news = espn_news[0:2]

	if id == 2 and num_of_articles > 18 and num_of_articles <= 36:
		news_list = news_list[20:fantasy_ind]
		if yahoo_ind >= 5:
			yahoo_news = yahoo_news[6:yahoo_ind]
		if espn_ind >= 2:
			espn_news = espn_news[4:espn_ind]
	elif id == 2 and num_of_articles <= 18:
		yahoo_news = []
		espn_news = []
		news_list = []

	if id == 3 and num_of_articles > 36 and num_of_articles <= 54:
		news_list = news_list[17:fantasy_ind]
		if yahoo_ind >= 11:
			yahoo_news = yahoo_news[11:yahoo_ind]
		if espn_ind >= 5:
			espn_news = espn_news[5:espn_ind]
	elif id == 3 and num_of_articles <= 36:
		yahoo_news = []
		espn_news = []
		news_list = []

	if id == 4 and num_of_articles > 54 and num_of_articles <= 72:
		news_list = news_list[26:fantasy_ind]
		if yahoo_ind >= 17:
			yahoo_news = yahoo_news[17:yahoo_ind]
		if espn_ind >= 8:
			espn_news = espn_news[8:espn_ind]
	elif id == 4 and num_of_articles <= 54:
		yahoo_news = []
		espn_news = []
		news_list = []

	if id == 5 and num_of_articles > 72 and num_of_articles <= 90:
		news_list = news_list[8:fantasy_ind]
		if yahoo_ind >= 26:
			yahoo_news = yahoo_news[26:yahoo_ind]
		if espn_ind >= 11:
			espn_news = espn_news[11:espn_ind]
	elif id == 5 and num_of_articles <= 72:
		yahoo_news = []
		espn_news = []
		news_list = []
	# contains the all content to be rendered in html. 

	context = {
		'news_list':news_list[:],
		'yahoo_news':yahoo_news[:],
		'espn_news':espn_news[:],
		'form':form,
	}

	# filters search results based off of what was received in a post request.
	# html form allows user to filter news feed by player name, team name, coach, analyst or source.
	if request.method == 'POST':
		# the following code removes articles from the context that do not contain the name or source that the user searches
		form = FilterForm(request.POST)
		if form.is_valid():
			player = form.cleaned_data['player_or_team'] 
			sources = form.cleaned_data['news_source']
			if sources != []: 
				if 'FantasyPros' not in sources:
					context.pop('news_list')
				if 'ESPN' not in sources:
					context.pop('espn_news')
				if 'Yahoo' not in sources:
					context.pop('yahoo_news')
			if player != '':
				name = player.split()
				for src in context:
					if src != 'form':
						for article in context[src][:]:
							print(article[0])
							if player not in article[0] and name[0] not in article[0].split() and name[1] not in article[0].split():
								context[src].remove(article)
			# if search fails, an error message is displayed along with the default page. 				
			if len(context.keys()) == 1:
				failed_search = True 
				context = {
					'news_list':news_list[:],
					'yahoo_news':yahoo_news[:],
					'espn_news':espn_news[:],
					'form':form,
					'failed_search': failed_search,
				}
			return render(request, 'news/news.html', context)

	return render(request, 'news/news.html', context)

# page that takes a given player and returns predicted performance.
def predictions_page(request):
	form = PredictionForm()
	if request.method == 'POST':
		form = PredictionForm(request.POST)
		if form.is_valid():
			player = form.cleaned_data['player']

			# calls function from news/webscrape.py that extracts data for the prediction algorithm.
			result = search_player(player)
			# calls function from news/predictions.py that predicts performance
			prediction = predictions(result[0], result[1], result[2])

			context = {'form':form, 'prediction':round(prediction[0]),'player':player, 'src':result[3]}
			return render(request, 'news/predictions.html', context)

	context = {'form':form}
	return render(request, 'news/predictions.html', context)

def rankings_page(request):

	# pulls weekly projections from database and appends them to the projections array.
	projections = []
	for i in list(Player.objects.all()):
		projections.append([i.name,i.current_projection])

	# copy of preseason predictions 
	names_copy = names.copy()

	count = 0
	for i in names:
		count += 1
		if count > 67:
			names_copy.pop(i)	

	context = {'names':names_copy, 'projections':projections}
	return render(request, 'news/rankings.html',context)

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
			player = Player(name=i[0], current_projection=int(round(i[1][0])))
			player.save()
		else:
			break
	return None

if datetime.datetime.now().strftime("%a") == 'Wed':
	update_database()