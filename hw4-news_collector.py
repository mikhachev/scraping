'''
Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.

Для парсинга использовать xpath. Структура данных должна содержать:
•	название источника,
•	наименование новости,
•	ссылку на новость,
•	дата публикации

'''

# В текущем виде просматривает только yandex и mail, продолжаю работать

from pprint import pprint
from lxml import html
import requests
import pandas as pd
from datetime import datetime
import time

pd.options.display.width = 0
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
            news_data = {}
            news_data['source'] = 'yandex.ru'
            news_data['name'] = root.xpath("//li[@class = 'list__item  list__item_icon']/a"
                                           "//span[@class = 'news__item-content']/text()")[cnt]
            news_data['link'] = root.xpath("//li[@class = 'list__item  list__item_icon']/a/@href")[cnt]

            ts = int(news_data['link'].split('&')[3].split('t=')[1])

            news_data['datetime'] = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            news.append(news_data)

            #print(news_data['name'])
            #print(news_data['link'])
            #print(news_data['datetime'])
            cnt += 1

    else:
        print('tag ya1  not found')

        cnt_static = cnt
        result_list_dynamic = root.xpath("//ol[@class = 'list news__list news__animation-list']/li")
        if result_list_dynamic:
            for i in result_list_dynamic:
                # news_text= html.fromstring(i.text)
                news_data = {}
                news_data['source'] = 'yandex.ru'
                news_data['name'] = root.xpath(
                    "/html/body//ol[@class = 'list news__list news__animation-list']/li"
                    "//span[@class = 'news__item-content']/text()")[cnt - cnt_static]
                news_data['link'] = \
                root.xpath("/html/body//ol[@class = 'list news__list news__animation-list']//a/@href")[cnt - cnt_static]

                ts = int(news_data['link'].split('&')[3].split('t=')[1])

                news_data['datetime'] = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                news.append(news_data)

                cnt += 1

        else:
            print('tag ya2  not found')

    return news


def mail_news():
    req = requests.get('https://mail.ru/',  headers=header)
    news = []
    news_data = {}
    root = html.fromstring(req.text)
    result_list = root.xpath("//div[@class = 'news-item__inner'] | //div[@class = 'news-item o-media news-item_media news-item_main']")
    cnt = 0

    if result_list:
        for i in result_list:

            news_data = {}
            news_data['source'] = 'mail.ru'
            news_data['name'] = root.xpath("//div[@class = 'news-item__inner']//a[not (@class) ]/text()"
                                           "|//h3/text()")[cnt]
            news_data['link'] = root.xpath("//div[@class = 'news-item__inner']//a[not (@class) ]/@href |"
                                           "//div[@class = 'news-item o-media news-item_media news-item_main']//a[1]/@href")[cnt]

            news_page_req = requests.get(news_data['link'],  headers=header)
            root_news = html.fromstring(news_page_req.text)
            result_news_time = root_news.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime "
                                               "| //span[@class='breadcrumbs__item js-ago']/@datetime")

            result_news_time = result_news_time[0].split('+')[0].replace('T', ' ')

            news_data['datetime'] = result_news_time
            news.append(news_data)
            if cnt > 15:
                break

            cnt += 1
            time.sleep(0.2)

    else:
        print('tag mail not found')

    return news

months = {'января':'01', 'февраля':'02', 'марта':'03', 'апреля':'04', 'мая':'05', 'июня':'06',
          'июля':'07', 'августа':'08', 'сентября':'09', 'октября':'10', 'ноября':'11', 'декабря':'12'}

def lenta_time_convert(ts):
    ts = ts.lstrip().split(',')
    ts[1] = ts[1].lstrip().split()
    ts[1][1] = months.get(ts[1][1])
    ts[1] = '-'.join(ts[1])
    ts.reverse()
    return ' '.join(ts)

def lenta_news():
        lenta_url = 'https://m.lenta.ru/'
        req = requests.get(lenta_url, headers=header)
        news = []

        root = html.fromstring(req.text)
        result_list = root.xpath("//li[@class = 'b-list-item b-list-item_news']/a")
        cnt = 0

        if result_list:
            for i in result_list:
                news_data = {}
                news_data['source'] = 'lenta.ru'
                news_data['name'] = root.xpath("//li[@class = 'b-list-item b-list-item_news']/a/"
                                               "span[@class = 'b-list-item__title']/text()")[cnt]
                news_data['link'] = lenta_url + root.xpath("//li[@class = 'b-list-item b-list-item_news']/a/@href")[cnt]
                #print(root.xpath("//li[@class = 'b-list-item b-list-item_news']/a/span/@datetime"))
                ts = root.xpath("//li[@class = 'b-list-item b-list-item_news']/a/span/time[@class = 'g-time']/"
                                "@datetime")[cnt]

                ts = lenta_time_convert(ts)
                ts = datetime.strptime(ts, '%d-%m-%Y %H:%M')
                news_data['datetime'] = ts
                #news_data['datetime'] =ts
                news.append(news_data)
                # news[cnt] = news_data
                cnt += 1
                if cnt > 10:
                    break
                #time.sleep(0.1)

        else:
            print('tag lenta not found')


        return news


def search_news():

    df1 = pd.DataFrame.from_dict(yandex_news())
    df2 = pd.DataFrame.from_dict(mail_news())
    df3 = pd.DataFrame.from_dict(lenta_news())
    #pprint(pd.DataFrame(yandex_news()))
    #pprint(pd.DataFrame(mail_news()))
    #pprint(pd.DataFrame(lenta_news()))
    df = pd.concat([df1, df2, df3], ignore_index= True)
    pprint(df)

search_news()

'''  Вывод программы:
       source                                               name                                               link             datetime
0   yandex.ru  Посольство Израиля в России объявило о своём в...  https://yandex.ru/news/story/Posolstvo_Izraily...  2019-10-30 09:49:14
1   yandex.ru         Российские военные развернули «Подсолнухи»  https://yandex.ru/news/story/Rossijskie_voenny...  2019-10-30 09:49:14
2   yandex.ru  Стрельбе в воинской части Забайкалья предшеств...  https://yandex.ru/news/story/Strelbe_v_voinsko...  2019-10-30 09:49:14
3   yandex.ru  Россияне назвали средний размер пенсии для дос...  https://yandex.ru/news/story/Rossiyane_nazvali...  2019-10-30 09:49:14
4     mail.ru  Посольства Израиля по всему миру закрылись из-...  https://news.mail.ru/politics/39293541/?fromma...  2019-10-30 12:17:16
5     mail.ru  Старейшая жительница России скончалась в возра...  https://news.mail.ru/society/39292129/?frommail=1  2019-10-30 10:43:38
6     mail.ru        Россияне назвали лучшие города для переезда  https://news.mail.ru/society/39290793/?frommail=1  2019-10-30 10:27:20
7     mail.ru  Названы причины расстрела солдат сослуживцем в...  https://news.mail.ru/incident/39288251/?fromma...  2019-10-30 08:23:36
8     mail.ru  Молодой человек с тапочками стал героем мемов ...  https://news.mail.ru/society/39293750/?frommai...  2019-10-30 12:15:56
9     mail.ru  Мужчина 13 лет играл в лотерею с одинаковыми ч...  https://news.mail.ru/society/39291679/?frommai...  2019-10-30 10:43:36
10    mail.ru  Ученые: через 30 лет в зоне затопления окажутс...  https://news.mail.ru/society/39291972/?frommai...  2019-10-30 10:43:33
11    mail.ru  Елизавета II нарушила королевский протокол во ...  https://news.mail.ru/society/39288210/?frommai...  2019-10-30 06:03:52
12    mail.ru  Стало известно о крупнейшей утечке данных банк...  https://news.mail.ru/incident/39288386/?fromma...  2019-10-30 08:32:10
13    mail.ru  В небе над Шотландией появилась четырехкратная...  https://news.mail.ru/society/39293119/?frommai...  2019-10-30 11:40:23
14    mail.ru  Экономисты предложили раздавать рецептурные ле...  https://news.mail.ru/society/39288806/?frommail=1  2019-10-30 11:52:22
15    mail.ru                  Почему США признали геноцид армян  https://news.mail.ru/politics/39288185/?fromma...  2019-10-30 03:57:04
16    mail.ru  Заявление Трампа о смерти лидера ИГ вызвало не...  https://news.mail.ru/politics/39288117/?fromma...  2019-10-30 06:36:40
17    mail.ru           Ефимова показала новое фото в купальнике       https://sportmail.ru/article/water/39284280/  2019-10-29 17:35:59
18    mail.ru     AG 20 — новый российский супервездеход (видео)  https://auto.mail.ru/article/75024-ag_20_novyi...  2019-10-29 10:55:19
19    mail.ru  Звезда «Уральских пельменей» объявила об уходе...  https://kino.mail.ru/news/52365_yuliya_mihalko...  2019-10-30 11:00:00
20   lenta.ru  Расстрелявшего сослуживцев в Забайкалье солдат...        https://m.lenta.ru//news/2019/10/30/toilet/  2019-10-30 12:29:00
21   lenta.ru  В Госдуму внесен законопроект о наказании за п...     https://m.lenta.ru//news/2019/10/30/nakazanie/  2019-10-30 12:58:00
22   lenta.ru  Российская восьмиклассница совершила самоубийство      https://m.lenta.ru//news/2019/10/30/bad_news/  2019-10-30 12:56:00
23   lenta.ru        Банду Шишкана заподозрили в новых убийствах      https://m.lenta.ru//news/2019/10/30/shishkun/  2019-10-30 12:55:00
24   lenta.ru  Фадеев уволил всех артистов своего лейбла и ра...   https://m.lenta.ru//news/2019/10/30/freedobbies/  2019-10-30 12:55:00
25   lenta.ru  Отец устроившего бойню в Забайкалье солдата оц...       https://m.lenta.ru//news/2019/10/30/neveryu/  2019-10-30 12:51:00
26   lenta.ru  Скорбящих на поминках случайно угостили кексом...          https://m.lenta.ru//news/2019/10/30/cake/  2019-10-30 12:42:00
27   lenta.ru  В Москве водитель насобирал более 400 штрафов ...  https://m.lenta.ru/https://moslenta.ru/news/v-...  2019-10-30 12:41:00
28   lenta.ru  Исчезнувший после шумного застолья с друзьями ...  https://m.lenta.ru//news/2019/10/30/food_city_...  2019-10-30 12:39:00
29   lenta.ru            Все посольства Израиля в мире закрылись    https://m.lenta.ru//news/2019/10/30/israel_emb/  2019-10-30 12:17:00
30   lenta.ru  Поводом для бойни в Забайкалье назвали попытку...           https://m.lenta.ru//news/2019/10/30/moy/  2019-10-30 12:56:00

Process finished with exit code 0


'''
