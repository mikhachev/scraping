#  На сейчас готово не полностью - только hh, но сегодня (21 окт. планирую завершить)
from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd
from pprint import pprint
text = input('Введите вакансию: ')
text = text.replace(' ', '+')
page = int(input('Введите кол-во страниц: '))

def hh_search(text, page):

    user_agent = {'User-agent': 'Mozilla/5.0'}
    link_hh = ('https://spb.hh.ru/search/vacancy?enable_snippets=true&')
    #main_link = ('localhost/hh.html/')
    i = 0
    vacs = []
    for p in range(page):
        html = requests.get(f'{link_hh}&text={text}&page={p}',  headers = user_agent).text
        parsed_html = bs(html,'lxml')
        vac_list = parsed_html.findAll('div', {'class':'vacancy-serp-item__row vacancy-serp-item__row_header'})
        df = pd.DataFrame(columns=['name', 'salary_min', 'salary_max', 'url', 'site'])

        for vac in vac_list:
            #print(i)
            vac_data = {}

            main_info = vac.findChild()
            link = vac.find('a')
            if not link:
                url = ''
                vac_data['name'] = ''
            else:
                vac_data['name'] = link.getText()
                url = link["href"]

            #print('vac_name', vac_data['name'] )
            #print('link', link)
            #print('url', url)

            compensation = vac.findParent().find('div', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            salary = 0
            salary_min = 0
            salary_max = 0
            if not compensation:
                salary = 0
            else:
                salary = compensation.getText()
                salary = re.sub(r"\s+", "", salary)
                if salary.find('от') >= 0 :
                    salary_min = re.findall(r'\d+',  salary)[0]
                elif salary.find('до') >= 0 :
                    salary_max = re.findall(r'\d+', salary)[0]
                elif salary.find('-') >= 0 :
                    salary = re.findall(r'\d+', salary)
                    salary_min = salary[0]
                    salary_max = salary[1]

                #print('sal', salary)
                #print('salary_min', salary_min)
                #print('salary_max', salary_max)
                vac_data['salary_min'] = salary_min
                vac_data['salary_max'] = salary_max
                vac_data['url'] = url
                vac_data['site'] = 'HeadHunter'

                vacs.append(vac_data)
                df.append(vac_data, ignore_index = True)

            i += 1
    return(vacs)

def sj_search(text, page):

    user_agent = {'User-agent': 'Mozilla/5.0'}
    link_hh = ('https://www.superjob.ru/vacancy/search/?')
    #main_link = ('localhost/hh.html/')
    i = 0
    vacs = []
    url_start = 'https://www.superjob.ru'
    url_end = '.html'
    for p in range(1, page+1):
        html = requests.get(f'{link_hh}&keywords={text}&page={p}',  headers = user_agent).text
        parsed_html = bs(html,'lxml')
        vac_list = parsed_html.findAll('div', {'class':'_3syPg _1_bQo _2FJA4'})
        df = pd.DataFrame(columns=['name', 'salary_min', 'salary_max', 'url', 'site'])

        for vac in vac_list:
            #print(i)
            vac_data = {}

            main_info = vac.findChild()
            #print('main_info', main_info)
            name = vac.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).getText()
            vac_data['name'] = name
            link = vac.find('a')

            if not link:
                url = ''

            else:
                url_vac = link['href']
                url = f'{url_start}/{url_vac}'
                vac_data['url'] = url

            salary = 0
            salary_min = 0
            salary_max = 0
            compensation = vac.find('span', {'class': '_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'})
            if not compensation:
                salary = 0
            else:
                salary = compensation.getText()
                if salary.find('от') >= 0:
                    salary_min = re.findall(r'\d+', salary)[0]
                #elif salary.find('до') >= 0:
                    #salary_max = re.findall(r'\d+', salary)[0]
                elif salary.find('—') >= 0:
                    salary = re.findall(r'\d+', salary)

                    salary_min = int(salary[0])*1000
                    salary_max = int(salary[2])*1000
                elif salary.find('договорённости') >= 0:
                    salary_min = 'по договорённости'


            #print('vac_name', vac_data['name'])
            #print('link', link)
            #print('url', url)
            #print('salary', salary)
            #print('salary_min', salary_min)
            #print('salary_max', salary_max)

            vac_data['salary_min'] = salary_min
            vac_data['salary_max'] = salary_max
            vac_data['url'] = url
            vac_data['site'] = 'Superjob'
            vacs.append(vac_data)
            df.append(vac_data, ignore_index=True)
            i += 1
    return (vacs)





'''
    compensation = vac.findParent().find('div', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    salary = 0
    salary_min = 0
    salary_max = 0
    if not compensation:
        salary = 0
    else:
        salary = compensation.getText()
        salary = re.sub(r"\s+", "", salary)
        if salary.find('от') >= 0 :
            salary_min = re.findall(r'\d+',  salary)[0]
        elif salary.find('до') >= 0 :
            salary_max = re.findall(r'\d+', salary)[0]
        elif salary.find('-') >= 0 :
            salary = re.findall(r'\d+', salary)
            salary_min = salary[0]
            salary_max = salary[1]

        print('sal', salary)
        print('salary_min', salary_min)
        print('salary_max', salary_max)
        vac_data['salary_min'] = salary_min
        vac_data['salary_max'] = salary_max
        vac_data['url'] = url
        vac_data['site'] = 'HeadHunter'
'''


                #df.append(vac_data, ignore_index = True)






def search_vac(text, page):
    print(hh_search(text, page))
    print(sj_search(text, page))
    df1 = pd.DataFrame.from_dict(hh_search(text, page))
    df2 = pd.DataFrame.from_dict(sj_search(text, page))
    df = pd.concat([df1, df2], ignore_index=True)
    print(df1)
    print(df2)
    return df
#df = pd.DataFrame(data=vacs)
#print(df)
print(search_vac(text, page))

'''

Выдача:
                                                 name  ...                                                url
0                                     Python Engineer  ...    https://spb.hh.ru/vacancy/34128405?query=python
1                                  Программист Python  ...    https://spb.hh.ru/vacancy/34145172?query=python
2                        QA Engineer (Тестировщик ПО)  ...    https://spb.hh.ru/vacancy/33925503?query=python
3                         Front-End React.js Engineer  ...    https://spb.hh.ru/vacancy/34128413?query=python
4                          Backend Developer (Python)  ...    https://spb.hh.ru/vacancy/33729628?query=python
5                                     PHP-программист  ...    https://spb.hh.ru/vacancy/33191231?query=python
6                              QA Automation Engineer  ...    https://spb.hh.ru/vacancy/32371003?query=python
7                                     PHP-разработчик  ...    https://spb.hh.ru/vacancy/34079849?query=python
8                                  Программист Python  ...    https://spb.hh.ru/vacancy/34198397?query=python
9                                    Python developer  ...    https://spb.hh.ru/vacancy/34005432?query=python
10                               Python Web Developer  ...    https://spb.hh.ru/vacancy/33895741?query=python
11                                 Программист Python  ...    https://spb.hh.ru/vacancy/33833014?query=python
12                                   Python developer  ...    https://spb.hh.ru/vacancy/33811537?query=python
13                              Python Data Scientist  ...    https://spb.hh.ru/vacancy/33840192?query=python
14                                 Разработчик Python  ...    https://spb.hh.ru/vacancy/33828496?query=python
15                                 Python-разработчик  ...    https://spb.hh.ru/vacancy/34200903?query=python
16                          Junior python-разработчик  ...    https://spb.hh.ru/vacancy/33725095?query=python
17                            Методист-эксперт Python  ...    https://spb.hh.ru/vacancy/33842117?query=python
18                                 Разработчик Python  ...    https://spb.hh.ru/vacancy/33571142?query=python
19                                   Python developer  ...    https://spb.hh.ru/vacancy/33271493?query=python
20                     Computer vision data scientist  ...    https://spb.hh.ru/vacancy/34068961?query=python
21                                   Python developer  ...    https://spb.hh.ru/vacancy/34182123?query=python
22                                 Программист Python  ...    https://spb.hh.ru/vacancy/34008673?query=python
23                                 Программист Python  ...  https://www.superjob.ru//vakansii/programmist-...
24      Администратор тестовых сред (ведущий инженер)  ...  https://www.superjob.ru//vakansii/administrato...
25                             Разработчик баз данных  ...  https://www.superjob.ru//vakansii/razrabotchik...
26                      Системный администратор Linux  ...  https://www.superjob.ru//vakansii/sistemnyj-ad...
27                           Аналитик data governance  ...  https://www.superjob.ru//vakansii/analitik-dat...
28  Системный архитектор / Главный конструктор (ра...  ...  https://www.superjob.ru//vakansii/sistemnyj-ar...
29                     Инженер администрирования сети  ...  https://www.superjob.ru//vakansii/inzhener-adm...
30  Педагог дополнительного образования (программи...  ...  https://www.superjob.ru//vakansii/pedagog-dopo...
31                            Системный администратор  ...  https://www.superjob.ru//vakansii/sistemnyj-ad...
32  Data Scientist отдела аудита информационных те...  ...  https://www.superjob.ru//vakansii/data-scienti...
33                            Инженер-программист SQL  ...  https://www.superjob.ru//vakansii/inzhener-pro...
34                        Старший сетевой инженер ЦОД  ...  https://www.superjob.ru//vakansii/starshij-set...
35                   Инженер (Linux) / Linux Embedded  ...  https://www.superjob.ru//vakansii/inzhener-325...
36  ГИС-специалист, специалист по цифровой картогр...  ...  https://www.superjob.ru//vakansii/gis-speciali...
37                      Системный администратор Linux  ...  https://www.superjob.ru//vakansii/sistemnyj-ad...
38                                     Data scientist  ...  https://www.superjob.ru//vakansii/data-scienti...
39  Системный аналитик / Ведущий системный админис...  ...  https://www.superjob.ru//vakansii/sistemnyj-an...
40                              Senior Java developer  ...  https://www.superjob.ru//vakansii/senior-java-...
41                              Старший преподаватель  ...  https://www.superjob.ru//vakansii/starshij-pre...
42                          Инженер-проектировщик ОДД  ...  https://www.superjob.ru//vakansii/inzhener-pro...

[43 rows x 5 columns]


'''


