# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join

class WorkparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    try:
        salary_min = scrapy.Field()
    except:
        salary_min = float('nan')
    try:
        salary_max = scrapy.Field()
    except:
        salary_max = float('nan')
    link = scrapy.Field()
    resource = scrapy.Field()

#output_processor=TakeFirst