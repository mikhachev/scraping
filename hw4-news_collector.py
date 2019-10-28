'''
Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.

Для парсинга использовать xpath. Структура данных должна содержать:
•	название источника,
•	наименование новости,
•	ссылку на новость,
•	дата публикации

'''

# В текущем виде просматривает только яндекс, продолжаю работать

from pprint import pprint
from lxml import html
import requests
from datetime import datetime

header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

def yandex_news():
    req = requests.get('https://yandex.ru/',  headers=header)
    news = []
    news_data = {}
    root = html.fromstring(req.text)
    result_list = root.xpath("/html/body//li[@class = 'list__item  list__item_icon']/a")
    cnt = 0

    if result_list:
        for i in result_list:
            #news_text= html.fromstring(i.text)
            news_data['source'] = 'yandex.ru'
            news_data['name'] = root.xpath("/html/body//li[@class = 'list__item  list__item_icon']/a"
                                           "//span[@class = 'news__item-content']/text()")[cnt]
            news_data['link'] = root.xpath("/html/body//li[@class = 'list__item  list__item_icon']/a/@href")[cnt]

            ts = int(news_data['link'].split('&')[3].split('t=')[1])

            news_data['datetime'] = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            news.append(news_data)

            #print(news_data['name'])
            #print(news_data['link'])
            #print(news_data['datetime'])
            cnt += 1

    else:
        print('tag1  not found')

    cnt_static = cnt
    result_list_dynamic = root.xpath("/html/body//ol[@class = 'list news__list news__animation-list']/li")
    if result_list_dynamic:
        for i in result_list_dynamic:
            # news_text= html.fromstring(i.text)
            news_data['source'] = 'yandex.ru'
            news_data['name'] = root.xpath(
                "/html/body//ol[@class = 'list news__list news__animation-list']/li"
                "//span[@class = 'news__item-content']/text()")[cnt-cnt_static]
            news_data['link'] = root.xpath("/html/body//ol[@class = 'list news__list news__animation-list']//a/@href")[cnt-cnt_static]

            ts = int(news_data['link'].split('&')[3].split('t=')[1])

            news_data['datetime'] = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            news.append(news_data)
            #print(news_data['name'])
            #print(news_data['link'])
            #print(news_data['datetime'])
           # print(news_data['link'])
            cnt += 1

    else:
        print('tag2  not found')

        #print(news_data)

    return news






'''
    # films_list = root.xpath("//div[contains(@class, 'filmsListNew')]/div")
    hrefs = root.xpath('//div[@class="name"]/a/@href')
    names = root.xpath('//div[@class="name"]/a/text()')
    genre = root.xpath('//div[@class="gray"][last()]/text()')
    rating = root.xpath('//div[@class="rating"]/span/text()')
    pprint(hrefs)
    
'''

pprint(yandex_news())


'''  Вывод программы:
I:\Study\ML-Python\GB\venv\Scripts\python.exe I:/Study/ML-Python/GB/Scraping/4/hw4-news_collector.py
[{'datetime': '2019-10-28 12:24:09',
  'link': 'https://yandex.ru/news/story/Sud_prigovoril_ehks-premera_Dagestana_k_65_godam_tyurmy_za_rastratu--e971cb4c963291d2f11260055cf4c9dd?lang=ru&from=main_portal&stid=wWf0TiWsT_HcAmeIMNaN&t=1572265449&lr=2&msid=1572266235.02307.140564.2485&mlid=1572265449.glob_225.e971cb4c',
  'name': 'Суд приговорил экс-премьера Дагестана к 6,5 годам тюрьмы за '
          'растрату',
  'source': 'yandex.ru'},
 {'datetime': '2019-10-28 12:24:09',
  'link': 'https://yandex.ru/news/story/Sud_prigovoril_ehks-premera_Dagestana_k_65_godam_tyurmy_za_rastratu--e971cb4c963291d2f11260055cf4c9dd?lang=ru&from=main_portal&stid=wWf0TiWsT_HcAmeIMNaN&t=1572265449&lr=2&msid=1572266235.02307.140564.2485&mlid=1572265449.glob_225.e971cb4c',
  'name': 'Суд приговорил экс-премьера Дагестана к 6,5 годам тюрьмы за '
          'растрату',
  'source': 'yandex.ru'},
 {'datetime': '2019-10-28 12:24:09',
  'link': 'https://yandex.ru/news/story/Sud_prigovoril_ehks-premera_Dagestana_k_65_godam_tyurmy_za_rastratu--e971cb4c963291d2f11260055cf4c9dd?lang=ru&from=main_portal&stid=wWf0TiWsT_HcAmeIMNaN&t=1572265449&lr=2&msid=1572266235.02307.140564.2485&mlid=1572265449.glob_225.e971cb4c',
  'name': 'Суд приговорил экс-премьера Дагестана к 6,5 годам тюрьмы за '
          'растрату',
  'source': 'yandex.ru'},
 {'datetime': '2019-10-28 12:24:09',
  'link': 'https://yandex.ru/news/story/Sud_prigovoril_ehks-premera_Dagestana_k_65_godam_tyurmy_za_rastratu--e971cb4c963291d2f11260055cf4c9dd?lang=ru&from=main_portal&stid=wWf0TiWsT_HcAmeIMNaN&t=1572265449&lr=2&msid=1572266235.02307.140564.2485&mlid=1572265449.glob_225.e971cb4c',
  'name': 'Суд приговорил экс-премьера Дагестана к 6,5 годам тюрьмы за '
          'растрату',
  'source': 'yandex.ru'},
 {'datetime': '2019-10-28 12:24:09',
  'link': 'https://yandex.ru/news/story/Sud_prigovoril_ehks-premera_Dagestana_k_65_godam_tyurmy_za_rastratu--e971cb4c963291d2f11260055cf4c9dd?lang=ru&from=main_portal&stid=wWf0TiWsT_HcAmeIMNaN&t=1572265449&lr=2&msid=1572266235.02307.140564.2485&mlid=1572265449.glob_225.e971cb4c',
  'name': 'Суд приговорил экс-премьера Дагестана к 6,5 годам тюрьмы за '
          'растрату',
  'source': 'yandex.ru'},
 {'datetime': '2019-10-28 12:24:09',
  'link': 'https://yandex.ru/news/story/Sud_prigovoril_ehks-premera_Dagestana_k_65_godam_tyurmy_za_rastratu--e971cb4c963291d2f11260055cf4c9dd?lang=ru&from=main_portal&stid=wWf0TiWsT_HcAmeIMNaN&t=1572265449&lr=2&msid=1572266235.02307.140564.2485&mlid=1572265449.glob_225.e971cb4c',
  'name': 'Суд приговорил экс-премьера Дагестана к 6,5 годам тюрьмы за '
          'растрату',
  'source': 'yandex.ru'},
 {'datetime': '2019-10-28 12:24:09',
  'link': 'https://yandex.ru/news/story/Sud_prigovoril_ehks-premera_Dagestana_k_65_godam_tyurmy_za_rastratu--e971cb4c963291d2f11260055cf4c9dd?lang=ru&from=main_portal&stid=wWf0TiWsT_HcAmeIMNaN&t=1572265449&lr=2&msid=1572266235.02307.140564.2485&mlid=1572265449.glob_225.e971cb4c',
  'name': 'Суд приговорил экс-премьера Дагестана к 6,5 годам тюрьмы за '
          'растрату',
  'source': 'yandex.ru'},
 {'datetime': '2019-10-28 12:24:09',
  'link': 'https://yandex.ru/news/story/Sud_prigovoril_ehks-premera_Dagestana_k_65_godam_tyurmy_za_rastratu--e971cb4c963291d2f11260055cf4c9dd?lang=ru&from=main_portal&stid=wWf0TiWsT_HcAmeIMNaN&t=1572265449&lr=2&msid=1572266235.02307.140564.2485&mlid=1572265449.glob_225.e971cb4c',
  'name': 'Суд приговорил экс-премьера Дагестана к 6,5 годам тюрьмы за '
          'растрату',
  'source': 'yandex.ru'},
 {'datetime': '2019-10-28 12:24:09',
  'link': 'https://yandex.ru/news/story/Sud_prigovoril_ehks-premera_Dagestana_k_65_godam_tyurmy_za_rastratu--e971cb4c963291d2f11260055cf4c9dd?lang=ru&from=main_portal&stid=wWf0TiWsT_HcAmeIMNaN&t=1572265449&lr=2&msid=1572266235.02307.140564.2485&mlid=1572265449.glob_225.e971cb4c',
  'name': 'Суд приговорил экс-премьера Дагестана к 6,5 годам тюрьмы за '
          'растрату',
  'source': 'yandex.ru'},
 {'datetime': '2019-10-28 12:24:09',
  'link': 'https://yandex.ru/news/story/Sud_prigovoril_ehks-premera_Dagestana_k_65_godam_tyurmy_za_rastratu--e971cb4c963291d2f11260055cf4c9dd?lang=ru&from=main_portal&stid=wWf0TiWsT_HcAmeIMNaN&t=1572265449&lr=2&msid=1572266235.02307.140564.2485&mlid=1572265449.glob_225.e971cb4c',
  'name': 'Суд приговорил экс-премьера Дагестана к 6,5 годам тюрьмы за '
          'растрату',
  'source': 'yandex.ru'}]

Process finished with exit code 0


'''
