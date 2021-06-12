# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from lxml import html


class HhruItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    salary = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    site = scrapy.Field()
    _id = scrapy.Field()


class SuperjobItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    salary = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    site = scrapy.Field()
    _id = scrapy.Field()


def process_price(price):
    correct_price = int(price.replace(' ', ''))
    return correct_price


def process_param(param):
    d = dict()
    param = html.fromstring(param)
    k = param.xpath("//dt/text()")[0]
    v = param.xpath("//dd/text()")
    d[k] = v
    return d


class LeroymerlinItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(process_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    params = scrapy.Field(input_processor=MapCompose(process_param))
    _id = scrapy.Field()


class InstaparserItem(scrapy.Item):
    name = scrapy.Field()
    user_id = scrapy.Field()
    photo = scrapy.Field()
    likes = scrapy.Field()
    post_data = scrapy.Field()
    _id = scrapy.Field()