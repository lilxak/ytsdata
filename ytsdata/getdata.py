import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')
# logging.disable(logging.CRITICAL)

def get_movie_rating(movie_title_selector, yts_parser):
    """ Returns a movie's rating from its title's selector """
    movie_page_link = yts_parser.select(movie_title_selector)[0]['href']
    try:
        movie_page = requests.get(movie_page_link)
    except:
        print('Cannot access to yts.lt. Please check your connexion.')
        return None
    else:
        movie_rating_selector = 'div.rating-row:nth-child(2) > span:nth-child(2)'
        parser = BeautifulSoup(movie_page.text, 'html.parser')
        rating = parser.select(movie_rating_selector)[0].text
        return rating
        
def get_movie_titles():
    """ Returns a list of latest YTS movies added """
    movies_titles = []
    movie_scores = []
    movie_title_selector = 'div.home-content:nth-child(1) > div:nth-child(1) > div:nth-child({}) > div:nth-child({}) > div:nth-child(2) > a:nth-child(1)'
    try:
        yts_page = requests.get('https://yts.lt/')
    except:
        print('Cannot access to yts.lt. Please check your connexion.')
        return None
    else:
        parser = BeautifulSoup(yts_page.text, 'html.parser')
        for i in [2,3]:
            for j in range(1,5):
                movies_titles.append(parser.select(movie_title_selector.format(i,j))[0].text)
                movie_scores.append(get_movie_rating(movie_title_selector.format(i,j), parser))
    logging.debug(movie_scores)
    return movies_titles

logging.debug(get_movie_titles())
