#  На сейчас готово не полностью - только hh, но сегодня (21 окт. планирую завершить)
from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd
from pprint import pprint
user_agent = {'User-agent': 'Mozilla/5.0'}
link_hh = ('https://spb.hh.ru/search/vacancy?enable_snippets=true&')
#main_link = ('localhost/hh.html/')
text = input('Введите вакансию: ')
text = text.replace(' ', '+')
page =  input('Введите кол-во страниц: ')
#req = requests.get(f'{main_link}&access_token={access_token}&user_id={user_id}', headers = headers)
html = requests.get(f'{link_hh}&text={text}&page={page}',  headers = user_agent).text
parsed_html = bs(html,'lxml')

vac_block = parsed_html.find('div',{'class':'vacancy-serp'})
vac_list = parsed_html.findAll('div', {'class':'vacancy-serp-item__row vacancy-serp-item__row_header'})
df = pd.DataFrame(columns=['name', 'salary_min', 'salary_max', 'url', 'site'])
#pprint(vac_list)
vacs = []
i=0
for vac in vac_list:
    print(i)
    vac_data = {}

    main_info = vac.findChild()
   # print('main_info', main_info)

    link = vac.find('a')
    if not link:
        url= ''
        vac_data['name'] = ''
    else:
        vac_data['name'] = link.getText()
        url = link["href"]

    print('vac_name', vac_data['name'] )
    print('link', link)
    print('url', url)

    compensation = vac.findParent().find('div', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    salary = 0
    salary_min = 0
    salary_max = 0
    if not compensation:
        salary = 0
    else:
        #salary = compensation
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






    vacs.append(vac_data)
    df.append(vac_data, ignore_index = True)

    i += 1
print('vacs', vacs)
#df = pd.DataFrame(data=vacs)
print(df)



