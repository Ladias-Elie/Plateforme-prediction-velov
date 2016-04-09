# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AllocineItem(scrapy.Item):
    date = scrapy.Field()
    cinema_name = scrapy.Field()
    cinema_adress = scrapy.Field()
    movie_name = scrapy.Field()
    movie_start = scrapy.Field()
    movie_end = scrapy.Field()
