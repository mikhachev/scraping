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
from datetime import datetime
import time

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
                # print(news_data['name'])
                # print(news_data['link'])
                # print(news_data['datetime'])
                # print(news_data['link'])
                cnt += 1

        else:
            print('tag2  not found')

        #print(news_data)

    return news


def mail_news():
    req = requests.get('https://mail.ru/',  headers=header)
    news = []
    news_data = {}
    root = html.fromstring(req.text)
    result_list = root.xpath("//div[@class = 'news-item__inner']")
    cnt = 0

    if result_list:
        for i in result_list:
            #news_text= html.fromstring(i.text)
            news_data = {}
            news_data['source'] = 'mail.ru'
            news_data['name'] = root.xpath("//div[@class = 'news-item__inner']//a[not (@class) ]/text()")[cnt]
            news_data['link'] = root.xpath("//div[@class = 'news-item__inner']//a[not (@class) ]/@href")[cnt]

            ts = int(time.time())
            news_data['datetime'] = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            news.append(news_data)
            #news[cnt] = news_data
            cnt += 1

    else:
        print('tag3  not found')

    #result_list = root.xpath("//div[@class='news-item o-media news-item_media news-item_main']")

    # Обработка главной новости
    news_data = {}
    news_data['source'] = 'mail.ru'
    news_data['name'] = root.xpath("//div[@class = 'news-item o-media news-item_media news-item_main']//h3/text()")[0]
    news_data['link'] = root.xpath("//div[@class = 'news-item o-media news-item_media news-item_main']//a[1]/@href")[0]
    ts = int(time.time())
    news_data['datetime'] = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    news.append(news_data)
    news[cnt] = news_data

    return news


def search_news():
    pprint(yandex_news())
    pprint(mail_news())

search_news()

'''  Вывод программы:
[{'datetime': '2019-10-28 14:46:47',
  'link': 'https://yandex.ru/news/story/Putin_i_Merkel_obsudili_tranzit_gaza_cherez_Ukrainu--2ddc36245bdd81b5934a3fe0e60143b5?lang=ru&from=main_portal&stid=16nsxspb-6yE2uavY5z8&t=1572274007&lr=2&msid=1572274852.40484.176928.2571&mlid=1572274007.glob_225.2ddc3624',
  'name': 'Путин и Меркель обсудили транзит газа через Украину',
  'source': 'yandex.ru'},
 {'datetime': '2019-10-28 14:46:47',
  'link': 'https://yandex.ru/news/story/V_Kremle_prokommentirovali_dannye_o_zakrytii_kompanij_malogo_biznesa--0cc468e534e284206826c7908cd9215f?lang=ru&from=main_portal&stid=fgA5I9g73fCSWzBBT_cE&t=1572274007&lr=2&msid=1572274852.40484.176928.2571&mlid=1572274007.glob_225.0cc468e5',
  'name': 'В Кремле прокомментировали данные о закрытии компаний малого '
          'бизнеса',
  'source': 'yandex.ru'},
 {'datetime': '2019-10-28 14:46:47',
  'link': 'https://yandex.ru/news/story/V_Kremle_ocenili_dannye_o_likvidacii_lidera_IG--0d0b11b05e497ae2232587a9f1be0da5?lang=ru&from=main_portal&stid=_P0tQ9y3l_ArIX-TO4s0&t=1572274007&lr=2&msid=1572274852.40484.176928.2571&mlid=1572274007.glob_225.0d0b11b0',
  'name': 'В Кремле оценили данные о ликвидации лидера ИГ',
  'source': 'yandex.ru'},
 {'datetime': '2019-10-28 14:46:47',
  'link': 'https://yandex.ru/news/story/Okhranniki_stali_samymi_zakreditovannymi_v_Rossii--f14d6e2ef404adae6edf6e47b1794a84?lang=ru&from=main_portal&stid=xJaQeBTsrjfdqWmLP-IT&t=1572274007&lr=2&msid=1572274852.40484.176928.2571&mlid=1572274007.glob_225.f14d6e2e',
  'name': 'Охранники стали самыми закредитованными в России',
  'source': 'yandex.ru'}]
[{'datetime': '2019-10-28 15:00:51',
  'link': 'https://news.mail.ru/politics/39269324/?frommail=1',
  'name': 'В\xa0Болгарии российского дипломата обвинили в\xa0шпионаже',
  'source': 'mail.ru'},
 {'datetime': '2019-10-28 15:00:51',
  'link': 'https://news.mail.ru/society/39263519/?frommail=1',
  'name': 'Роструд напомнил о короткой рабочей неделе\r\n',
  'source': 'mail.ru'},
 {'datetime': '2019-10-28 15:00:51',
  'link': 'https://news.mail.ru/incident/39268008/?frommail=1',
  'name': 'В\xa0Англии спасают мужчину, свисающего с\xa0вершины 90-метровой '
          'трубы',
  'source': 'mail.ru'},
 {'datetime': '2019-10-28 15:00:51',
  'link': 'https://news.mail.ru/society/39269141/?frommail=10',
  'name': 'Дочь годами писала сообщения покойному отцу и\xa0получила ответ',
  'source': 'mail.ru'},
 {'datetime': '2019-10-28 15:00:51',
  'link': 'https://news.mail.ru/incident/39259883/?frommail=10',
  'name': '«Темная история»: почему\xa0СК ищет семью, пропавшую 30 лет назад',
  'source': 'mail.ru'},
 {'datetime': '2019-10-28 15:00:51',
  'link': 'https://news.mail.ru/politics/39268813/?frommail=1',
  'name': 'Климкин призвал не\xa0допустить признания «Азова» террористами',
  'source': 'mail.ru'},
 {'datetime': '2019-10-28 15:00:51',
  'link': 'https://news.mail.ru/society/39265508/?frommail=10',
  'name': 'В\xa0соцсетях массово ищут кошку, спрятанную среди голубей',
  'source': 'mail.ru'},
 {'datetime': '2019-10-28 15:00:51',
  'link': 'https://news.mail.ru/economics/39267429/?frommail=1',
  'name': 'Стало известно, кто\xa0из россиян больше всех закредитован',
  'source': 'mail.ru'},
 {'datetime': '2019-10-28 15:00:51',
  'link': 'https://news.mail.ru/society/39266219/?frommail=1',
  'name': 'Опрос показал, сколько россиян считают США враждебной страной',
  'source': 'mail.ru'},
 {'datetime': '2019-10-28 15:00:51',
  'link': 'https://news.mail.ru/society/39269063/?frommail=10',
  'name': 'Художник мастерски объединяет животных и\xa0природу (фото)',
  'source': 'mail.ru'},
 {'datetime': '2019-10-28 15:00:51',
  'link': 'https://news.mail.ru/society/39261603/?frommail=10',
  'name': 'Найденный на\xa0кухне шедевр Чимабуэ продан за\xa024\xa0млн евро',
  'source': 'mail.ru'},
 {'datetime': '2019-10-28 15:00:51',
  'link': 'https://news.mail.ru/society/39264131/?frommail=10',
  'name': 'Спутник снял огромные атмосферные волны над\xa0Землей',
  'source': 'mail.ru'},
 {'datetime': '2019-10-28 15:00:51',
  'link': 'https://sportmail.ru/news/hockey-nhl/39267555/',
  'name': 'У\xa0Малкина нашли паспорт США. Документ всплыл из-за\xa0скандала',
  'source': 'mail.ru'},
 {'datetime': '2019-10-28 15:00:51',
  'link': 'https://auto.mail.ru/article/75015-samyi_dostupnyi_land_rover_prodazhi_nachalis/',
  'name': 'Самый доступный Land Rover: продажи начались',
  'source': 'mail.ru'},
 {'datetime': '2019-10-28 15:00:51',
  'link': 'https://kino.mail.ru/news/52354_harlamov_prokommentiroval_otkrovennie_stseni_asmus_v_kino/?from=mr_news',
  'name': 'Харламов отреагировал на откровенные киносцены с участием жены',
  'source': 'mail.ru'},
 {'datetime': '2019-10-28 15:00:51',
  'link': 'https://news.mail.ru/incident/39269360/?frommail=1',
  'name': 'Путин наградил бортпроводницу, спасшую людей из сгоревшего Ан-24',
  'source': 'mail.ru'}]
Process finished with exit code 0


'''
