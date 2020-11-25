from django.shortcuts import render, redirect
from django.http import HttpResponse

from .webscrape import get_fantasy, get_yahoo, get_espn, search_player
from .forms import FilterForm, PredictionForm
from .predictions import predictions
from .names import names
from .models import Player, Article
import datetime


# updates the database every week
def update_database():
	projections = []
	Player.objects.all().delete()
	for name in names.keys():
		try:
			result = search_player(name)
			prediction = predictions(result[0], result[1], result[2])
			projections.append([name, prediction])
			print(result)
		except:
			continue 

	def by_projection(item):
		return item[1]

	projections.sort(key=by_projection)
	for i in projections[::-1]:
		if i[1] > 0:
			player = Player(name=i[0], current_projection=int(round(i[1][0])))
			print(player)
			player.save()
		else:
			break

# the following functions determine what gets rendered on different pages of the website.

def update_page(request):
	fantasy_pros = get_fantasy()
	# yahoo = get_yahoo()
	# espn = get_espn()

	update_database()

	week = str(datetime.date.today())[:4] + '-' + str(datetime.date.today())[5:7]

	if len(Article.objects.all()) < 90:

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
	else:
		for article in list(Article.objects.all())[::-1]:
			if len(Article.objects.all()) > 90:
				article.delete()
			else:
				break
	print(Player.objects.all())
	return HttpResponse('<h1>Database updated</h1>')


# the home page contains news articles webscraped from several fantasy football websites and a form to filter these results.
def news_page(request, id=1):
	context = {}
	news_list = []
	[news_list.append([article.title, article.url, article.image_path]) for article in list(Article.objects.filter(source='fantasy')) if article.title not in news_list]

	yahoo_news = [[article.title, article.url] for article in list(Article.objects.filter(source='yahoo'))]

	espn_news = [[article.title, article.url] for article in list(Article.objects.filter(source='espn'))]

	form = FilterForm()

	if id == 1:

		news_list = news_list[0:9]
		yahoo_news = yahoo_news[0:6]
		espn_news = espn_news[0:2]
		context['week'] = Article.objects.get(title=news_list[0][0]).date

		print(context)

	if id == 2:


		new_list = []
		if len(news_list) > 9:
			count = 0
			for article in news_list[9:-1]:
				if count <= 9:
					new_list.append(article)
					count += 1
				else:
					break 
 		
		news_list = new_list

		new_list = []
		if len(yahoo_news) > 6:
			count = 0
			for article in yahoo_news[6:-1]:
				if count <= 6:
					new_list.append(article)
					count += 1
				else:
					break 

		yahoo_news = new_list

		new_list = []
		if len(espn_news) > 3:
			count = 0
			for article in espn_news[3:-1]:
				if count <= 3:
					new_list.append(article)
					count += 1
				else:
					break 
		espn_news = new_list

		if len(news_list) > 0:
				context['week'] = Article.objects.get(title=news_list[0][0]).date

	if id == 3:

		new_list = []
		if len(news_list) > 18:
			count = 0
			for article in news_list[18:-1]:
				if count <= 9:
					new_list.append(article)
					count += 1
				else:
					break 
 		
		news_list = new_list

		new_list = []
		if len(yahoo_news) > 12:
			count = 0
			for article in yahoo_news[12:-1]:
				if count <= 6:
					new_list.append(article)
					count += 1
				else:
					break 

		yahoo_news = new_list

		new_list = []
		if len(espn_news) > 6:
			count = 0
			for article in espn_news[6:-1]:
				if count <= 3:
					new_list.append(article)
					count += 1
				else:
					break 
		espn_news = new_list

		if len(news_list) > 0:
			context['week'] = Article.objects.get(title=news_list[0][0]).date

	if id == 4:

		new_list = []
		if len(news_list) > 27:
			count = 0
			for article in news_list[27:-1]:
				if count <= 9:
					new_list.append(article)
					count += 1
				else:
					break 
 		
		news_list = new_list

		new_list = []
		if len(yahoo_news) > 18:
			count = 0
			for article in yahoo_news[18:-1]:
				if count <= 6:
					new_list.append(article)
					count += 1
				else:
					break 

		yahoo_news = new_list

		new_list = []
		if len(espn_news) > 9:
			count = 0
			for article in espn_news[9:-1]:
				if count <= 3:
					new_list.append(article)
					count += 1
				else:
					break 
		espn_news = new_list

		if len(news_list) > 0:
			context['week'] = Article.objects.get(title=news_list[0][0]).date

	if id == 5:

		new_list = []
		if len(news_list) > 36:
			count = 0
			for article in news_list[36:-1]:
				if count <= 9:
					new_list.append(article)
					count += 1
				else:
					break 
	 		
		news_list = new_list

		new_list = []
		if len(yahoo_news) > 24:
			count = 0
			for article in yahoo_news[24:-1]:
				if count <= 6:
					new_list.append(article)
					count += 1
				else:
					break 

		yahoo_news = new_list

		new_list = []
		if len(espn_news) > 12:
			count = 0
			for article in espn_news[12:-1]:
				if count <= 3:
					new_list.append(article)
					count += 1
				else:
					break 
		espn_news = new_list

		if len(news_list) > 0:
			context['week'] = Article.objects.get(title=news_list[0][0]).date

	# contains the all content to be rendered in html. 

	
	context['news_list'] = news_list[:]
	context['yahoo_news'] = yahoo_news[:]
	context['espn_news'] = espn_news[:]
	context['form'] = form
	context['background'] = 'static/images/background.png'

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
					'week': Article.objects.get(title=news_list[0][0]).date,
					'background': 'static/images/background.png'
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

	print(Player.objects.all())
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



