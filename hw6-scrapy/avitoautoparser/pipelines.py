# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class AvitoparserPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

class DataBasePipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.scrapy_avito

    def process_item(self, item, spider):
        item['color'] = item['color'].strip()
        #item['generation'] = item['generation'].strip()
        item['kilometers'] = item['kilometers'].replace('\xa0', '').strip()
        #item['modify'] = item['modify'].strip()
        #item['transmission'] = item['transmission'].strip()
        item['year'] = int(item['year'])
        item['brend'] = item['brend'].strip()
        item['model'] = item['model'].strip()
        item['price'] = int(item['price'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item
74