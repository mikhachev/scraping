# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import scrapy


def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values

def clean_text(value):
    return value.strip(" ").strip("\n")

class AvitoAutoparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    price = scrapy.Field(output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    brend = scrapy.Field(output_processor=Join())
    model = scrapy.Field(output_processor=Join())
    #generation = scrapy.Field(input_processor=Join(), output_processor=MapCompose(clean_text))
    #modify =  scrapy.Field(input_processor=Join(), output_processor=MapCompose(clean_text))
    #transmission = scrapy.Field(input_processor=Join(), output_processor=MapCompose(clean_text))
    transmission = scrapy.Field(output_processor=Join())
    generation = scrapy.Field(output_processor=Join())
    modify = scrapy.Field(output_processor=Join())

    year = scrapy.Field(output_processor=Join())
    kilometers = scrapy.Field(output_processor=Join())

    color = scrapy.Field(output_processor=Join())
    link = scrapy.Field(output_processor=TakeFirst())

    pass
