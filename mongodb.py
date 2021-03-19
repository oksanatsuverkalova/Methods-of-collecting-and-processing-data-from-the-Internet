from pprint import pprint
import requests
from lxml import html
import datetime
from pymongo import MongoClient


my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}


def requests_lenta_news():
    url = 'https://lenta.ru'
    response = requests.get(f'{url}', headers=my_headers)
    root = html.fromstring(response.text)
    news_block = root.xpath("//div[contains(@class,'b-yellow-box__wrap')]/div[contains(@class, 'item')]")
    base_news = []
    for item in news_block:
        news = {}
        name_source = 'lenta.ru'
        name_news = item.xpath(".//a/text()")
        link_news_info = item.xpath(".//a/@href")
        link_news = f'{url}{link_news_info[0]}'
        response_2 = requests.get(link_news, headers=my_headers)
        root = html.fromstring(response_2.text)
        date_news_info = root.xpath(".//div[@class = 'b-topic__info']/time/@datetime")
        date_news = date_news_info[0][:10].split('-')
        date_news = datetime.date(int(date_news[0]), int(date_news[1]), int(date_news[2])).strftime('%d.%m.%Y')
        news['name_source'] = name_source
        news['name_news'] = name_news[0].replace(u'\xa0', ' ')
        news['link_news'] = link_news
        news['date_news'] = date_news

        base_news.append(news)

    return base_news


def requests_yandex_news():
    url = 'https://yandex.ru/news'
    response = requests.get(f'{url}', headers=my_headers)
    root = html.fromstring(response.text)
    news_block = root.xpath("//article[contains(@class,'mg-card')]//a[contains(@href,'rubric=science') and @class='mg-card__link']/ancestor::article")
    base_news = []
    for item in news_block:
        news = {}
        name_source = item.xpath(".//span[contains(@class, 'mg-card-source__source')]//text()")
        name_news = item.xpath(".//div[contains(@class, 'mg-card__text')]//h2/text()")
        link_news = item.xpath(".//div[contains(@class, 'mg-card__text')]/a/@href")
        date_news_info = item.xpath(".//span[contains(@class, 'mg-card-source__time')]/text()")

        try:
            yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%d.%m.%Y')
            date_news_info = date_news_info.replace('Вчера', yesterday)
        except AttributeError:
            today = datetime.date.today().strftime('%d.%m.%Y')
            date_news_info = f'{today} {date_news_info[0]}'

        news['name_source'] = name_source[0]
        news['name_news'] = name_news[0]
        news['link_news'] = link_news[0]
        news['date_news'] = date_news_info
        base_news.append(news)

    return base_news


def requests_mail_news():
    url = 'https://news.mail.ru/'
    response = requests.get(f'{url}', headers=my_headers)
    root = html.fromstring(response.text)
    news_block= root.xpath("//div[contains(@class,'daynews__')]/a | //ul[@data-module='TrackBlocks']/li[@class='list__item']/a")
    base_news = []

    for i, item in enumerate(news_block, 1):
        news = {}
        if i < 6:
            name_news = item.xpath(".//span[contains(@class, 'photo__title')]/text()")
        else:
            name_news = item.xpath(".//text()")
        link_news = item.xpath(".//@href")
        response_2 = requests.get(link_news[0], headers=my_headers)
        dom = html.fromstring(response_2.text)
        name_source = dom.xpath("//span[contains(@class, 'breadcrumbs__item')]//a//text()")
        date_news_info = dom.xpath("//span[contains(@class, 'breadcrumbs__item')]//span[contains(@class, 'note__text')]/@datetime")
        date_news = date_news_info[0][:10].split('-')
        date_news = datetime.date(int(date_news[0]), int(date_news[1]), int(date_news[2])).strftime('%d.%m.%Y')
        news['name_source'] = name_source[0]
        news['name_news'] = name_news[0].replace(u'\xa0', ' ')
        news['link_news'] = link_news[0]
        news['date_news'] = date_news
        base_news.append(news)

    return base_news


if __name__ == "__main__":
    lenta_news = requests_lenta_news()
    pprint(lenta_news)
    yandex_news = requests_yandex_news()
    pprint(yandex_news)
    mail_news = requests_mail_news()
    pprint(mail_news)
    client = MongoClient('localhost', 27017)
    db = client['News']
    news = db.news
    news.insert_many(lenta_news)
    news.insert_many(yandex_news)
    news.insert_many(mail_news)