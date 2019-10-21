from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd
from pprint import pprint
user_agent = {'User-agent': 'Mozilla/5.0'}
main_link = ('https://spb.hh.ru/')
#main_link = ('localhost/hh.html/')
html = requests.get(main_link+'search/vacancy?area=2&st=searchVacancy&text=Python+junior&from=suggest_post',  headers = user_agent).text
parsed_html = bs(html,'lxml')

vac_block = parsed_html.find('div',{'class':'vacancy-serp'})
#vac_list = vac_block.findChildren(recursive=False)
#vacs = parsed_html.findAll('div',{'class':'resume-search-item__name'})
#print('vac_list', vac_list)
#vac_list = parsed_html.findAll('div', {'class':'vacancy-serp-item'})
#vac_list = parsed_html.findAll('div', {'class':'vacancy-serp-item__row vacancy-serp-item__row_header'})
vac_list = parsed_html.findAll('div', {'class':'vacancy-serp-item__row vacancy-serp-item__row_header'})

#pprint(vac_list)
vacs = []
i=0
for vac in vac_list:
    print(i)
    vac_data = {}

    main_info = vac.findChild()
    #parent = vac.findParent()
    #print('parent', parent)
    print('main_info', main_info)

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

    i += 1
print('vacs', vacs)
df = pd.DataFrame(data=vacs)
df.head(5)
print(df)



