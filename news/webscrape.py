import requests
import lxml
from bs4 import BeautifulSoup
from collections import defaultdict
from .names import names


# function returns true if img is a jpg  
def is_jpg(img):
    if img[-3:-1] == 'jp':
        return True

# top news stories from fantasy pros
news_site = requests.get('https://www.fantasypros.com/nfl/articles/')
news_src = news_site.content
news_soup = BeautifulSoup(news_src, 'lxml')
articles = []
titles = []

# finds all a and div tags for each article's title, link, and thumbnail.
for article_tag in news_soup.find_all('a'):
    if article_tag.img and is_jpg(article_tag.img['src']):
        articles.append([article_tag['href'], article_tag.img['src']])


for div_tag in news_soup.find_all('div', {'class': 'eight columns'}):
    if div_tag.a:
        titles.append(div_tag.a.text.strip())

# creates a python dictionary with the information extracted above
news = {k: v for (k, v) in zip(titles, articles)}


# top news from yahoo 
result = requests.get('https://football.fantasysports.yahoo.com/')
src = result.content
soup = BeautifulSoup(src, 'lxml')

# The following code extracts the title, link, and thumbnail of all top stories and stores them in a 2d array.
yahoo_news = []
articles = soup.find('section', {'id': 'home-fantasy-headlines'})
for a_tag in articles.find_all('a'):
    yahoo_news.append([a_tag.text, a_tag['href']])


# top news from espn
espn_results = requests.get('https://www.espn.com/fantasy/football/')
espn_src = espn_results.content
espn_soup = BeautifulSoup(espn_src, 'lxml')

# The following code extracts the title, link, and thumbnail of all top stories and stores them in a 2d array.
espn_news = []
news_container = espn_soup.find('ul', {'class': 'headlineStack__list'})
for a_tag in news_container.find_all('a'):
    espn_news.append([a_tag.text, a_tag['href']])
    
# search for a player
def search_player(player):
    # the following searches fantasypros.com for the stats of a player, and returns information relevent to the prediction algorithm.
    first_last = player.split()
    search = 'https://www.fantasypros.com/nfl/players/' + first_last[0].lower() + '-' + first_last[1].lower() + '.php'
    result = requests.get(search)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    opponent = ''
    average = ''
    table1 = soup.find('table', {'class': 'table table-bordered sos'})
    for i in table1.find_all('td'):
        if 'th' in i.text:
            opponent += i.text[:2]
            break
    table2 = soup.find_all('table')
    for i in table2:
        if 'Statistics (avgs.)' in str(i.caption):
            table = i
            break

    td_tags = table.find_all('td')

    # code to determine the position of the player 
    position = soup.find_all('h5')[0].text
    position = position[0:2].lower()
    file = position + '.csv'

    # code to find the picture
    img = soup.find('img',{'alt':player})

    # in order, the return statment holds the average fantasy points per game, the rank of opponent, the file that the prediction algo will need to access, and the player's image.
    return [int(round(float(td_tags[-1].text))), int(opponent), file, img['src']]
