# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Info(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    info = scrapy.Field()


class ImageUrl(scrapy.Item):
    image_url = scrapy.Field()


class PageUrl(scrapy.Item):
    page_url = scrapy.Field()


class TagPage(scrapy.Item):
    tagName = scrapy.Field()
    tagId = scrapy.Field()
    tagTypeName = scrapy.Field()
    tagTypeID = scrapy.Field()
    albumIDList = scrapy.Field()

