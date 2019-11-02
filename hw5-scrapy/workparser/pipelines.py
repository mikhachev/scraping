
from pymongo import MongoClient
import re

class WorkparserPipeline(object):
    def __init__(self):

        client = MongoClient('localhost', 27017)
        self.mongo_base = client.scrapy_vacansy

    def process_item(self, item, spider):  # Сюда попадает item

        if item['resource'] == 'hh':
            item['link'] = item['link'].split('?')[0]
            item['salary'] = item['salary'].replace('\xa0', '')
            if not item["salary_min"]:
                pass
            else:
                try:
                    item["salary_min"] = int(item["salary_min"])
                except ValueError:
                    pass

            if not item["salary_max"]:
                pass
            else:
                try:
                    item["salary_max"] = int(item["salary_max"])
                except ValueError:
                    pass

        elif item['resource'] == 'sj':
            item['link'] = item['link']
            item['salary'] = item['salary'][0].replace('\xa0', '')
            item['salary'] = item['salary'].replace('<span class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc">', '')
            item['salary'] = item['salary'].replace('<span>', '')
            item['salary'] = item['salary'].replace('</span>', '')
            item['salary'] = item['salary'].replace('<!-- -->', '')
            item['salary'] = item['salary'].replace('₽', '')
            currency = 1
            if item['salary'].find('$') > 0:
                currency = 64
            if item['salary'].find('от') >= 0:
                item['salary_min'] = re.findall(r'\d+', item['salary'])[0]*currency
            elif item['salary'].find('до') >= 0:
                item['salary_max'] = re.findall(r'\d+', item['salary'])[0]*currency
            elif item['salary'] == re.findall(r'\d+', item['salary'])[0]:
                item['salary_max'] = item['salary']
                item['salary_min'] = item['salary']

            elif item['salary'].find('—') > 0 :
                #salary = re.findall(r'\d+', salary)
                item['salary_min'] = item['salary'].split('—')[0]*currency
                item['salary_max'] = item['salary'].split('—')[1]*currency


        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item




