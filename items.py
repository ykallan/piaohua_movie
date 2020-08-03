# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PiaohuaMovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_list = scrapy.Field()
    quanjilist = scrapy.Field()
    name = scrapy.Field()
    pianming = scrapy.Field()
    release_time = scrapy.Field()
    # item['movie_list'] = movielist
    # item['quanjilist'] = quanjilist
    # item['name'] = name
    # item['pianming'] = pianming
    # item['release_time'] = release_time
