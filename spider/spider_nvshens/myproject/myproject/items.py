# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Info(scrapy.Item):
    info = scrapy.Field()
    type = scrapy.Field()


class PageUrl(scrapy.Item):
    url = scrapy.Field()
    type = scrapy.Field()


class NoMatchUrl(scrapy.Item):
    url = scrapy.Field()
    type = scrapy.Field()


class TagPage(scrapy.Item):
    tagName = scrapy.Field()
    tagId = scrapy.Field()
    tagTypeName = scrapy.Field()
    tagTypeID = scrapy.Field()
    albumIDList = scrapy.Field()
    type = scrapy.Field()


class AlbumImage(scrapy.Item):
    star_id = scrapy.Field()
    album_id = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()


class AlbumCover(scrapy.Item):
    star_id = scrapy.Field()
    album_id = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()


class AlbumInfo(scrapy.Item):
    album_id = scrapy.Field()
    album_name = scrapy.Field()
    publish_date = scrapy.Field()
    description = scrapy.Field()
    company = scrapy.Field()
    tag_list = scrapy.Field()
    type = scrapy.Field()


class FailedURL(scrapy.Item):
    url = scrapy.Field()
    func = scrapy.Field()
    type = scrapy.Field()
