
from pymongo import MongoClient
import re

class WorkparserPipeline(object):
    def __init__(self):

        client = MongoClient('localhost', 27017)
        self.mongo_base = client.scrapy_vacansy

    def process_item(self, item, spider):  # Сюда попадает item

        if item['resource'][0] == 'hh':
            item['link'] = item['link'][0].split('?')[0]
            item['name'] = item['name'][1] #+' '+item['name'][2]
            item['resource'] = item['resource'][0]
            item['salary'] = item['salary'][0].replace('\xa0', '')
            try:
                item["salary_min"] = int(item["salary_min"][1])
            except:
                item["salary_min"] = float('nan')
            try:
                item["salary_max"] = int(item["salary_max"][1])
            except:
                item["salary_max"] = float('nan')


            '''
            if not item["salary_max"]:
                item["salary_max"] = float('nan')
            else:
                try:
                    item["salary_max"] = int(item["salary_max"][0])
                except ValueError:
                    item["salary_max"] = float('nan')
            pass
            '''

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
                item['salary_min'] = int(re.findall(r'\d+', item['salary'])[0])*currency
                item['salary_max'] = float('nan')
            elif item['salary'].find('договорённости') > 0:
                item['salary_min'] = float('nan')
                item['salary_max'] = float('nan')
            elif item['salary'].find('до') >= 0:
                item['salary_max'] = int(re.findall(r'\d+', item['salary'])[0]) * currency
                item['salary_min'] = float('nan')
            elif item['salary'] == re.findall(r'\d+', item['salary'])[0]:
                item['salary_max'] = int(item['salary'])
                item['salary_min'] = int(item['salary'])
            elif item['salary'].find('—') > 0 :
                item['salary_min'] = int(item['salary'].split('—')[0])*currency
                item['salary_max'] = int(item['salary'].split('—')[1])*currency





        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item




