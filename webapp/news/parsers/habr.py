import locale
import platform

from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from webapp.news.parsers.utils import get_html, save_news
from webapp.news.models import News
from webapp.db import db


if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, "russian")
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU')


def parse_habr_date(date_str):    
    try:
        return datetime.strptime(date_str, '%Y-%m-%d, %H:%M')
    except ValueError:
        return datetime.now()


def get_news_snippets():
    html = get_html("https://habr.com/ru/search/?target_type=posts&q=python&order_by=date")
    if html:        
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('div', class_='tm-articles-list')        
        all_news = all_news.findAll('article', class_='tm-articles-list__item')        
        
        for news in all_news:
            title = news.find('a', class_='tm-article-snippet__title-link').text
            url = news.find('a', class_='tm-article-snippet__title-link')['href']
            url = ''.join(['https://habr.com', url])
            published = news.find('time')['title']
            published = parse_habr_date(published)
            save_news(title, url, published)
            

def get_news_content():
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_text = soup.find('div', class_='tm-article-body').decode_contents()
            if news_text:
                news.text = news_text
                db.session.add(news)
                db.session.commit()
