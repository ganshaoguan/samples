# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    unit = scrapy.Field()
    square = scrapy.Field()
    house_type = scrapy.Field()
    height = scrapy.Field()
    orientation = scrapy.Field()
    location = scrapy.Field()
    business_region = scrapy.Field()
    village = scrapy.Field()
    traffic = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()