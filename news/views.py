from django.shortcuts import render, redirect
from django.http import HttpResponse

from .webscrape import news, yahoo_news, espn_news, search_player
from .forms import FilterForm, PredictionForm
from .predictions import predictions 
from .names import names
from .models import Player
import datetime


# the following functions determine what gets rendered on different pages of the website.

# the home page contains news articles webscraped from several fantasy football websites and a form to filter these results.
def news_page(request):

	news_list = []
	for (k,v) in news.items():
		news_list.append([k,v[0],v[1]])

	form = FilterForm()
	
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