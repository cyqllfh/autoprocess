# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MovieItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()

class FilmInfoItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    cinema = scrapy.Field()
    place_datail = scrapy.Field()
    g_price = scrapy.Field()
    b_price = scrapy.Field()

class DoubanLinkItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()

class DoubanMovieItem(scrapy.Item):
    name = scrapy.Field()
    director= scrapy.Field()
    rating_num = scrapy.Field()
    scriptwriters = scrapy.Field()
    actors = scrapy.Field()
    genres = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    descriptions = scrapy.Field()
    reviews = scrapy.Field()