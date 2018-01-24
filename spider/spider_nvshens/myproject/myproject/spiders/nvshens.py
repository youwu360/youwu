# -*- coding: utf-8 -*-
import threading

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import Info, NoMatchUrl, PageUrl, TagPage, AlbumImage, AlbumCover, FailedURL, AlbumInfo
from urllib.parse import urljoin
import time
from ..ProxyScrapyer import ProxyScrapyer
from .nvshens_url_match import NvshensURLMatcher
from scrapy.linkextractors import LinkExtractor
from urllib import parse
import re
import sys


class NvshensSpiderHelper(object):

    nvshens_spider = None

    def try_get_split_result(self, line, sep, index):
        if type(line) is str:
            arr = line.split(sep)
            if len(arr) > index:
                return arr[index]
        return None

    def try_xpath_extract(self, response, path):
        try:
            data = response.xpath(path).extract()
            return data
        except:
            return None

    def try_xpath_extract_first(self, response, path):
        data = self.try_xpath_extract(response, path)
        if type(data) is list and len(data) >= 1:
            return data[0]
        return None

    def parse_album_page(self, response):

        cur_page_url = response.url
        print("in parse_album_page *******************")
        print("response.url" + response.url)
        if not self.nvshens_spider.nvshens_url_matcher.match_pattern_album_page(response.url):
            print("response.url:" + response.url + " not match match_pattern_album_page")
            return
        print("response.url:" + response.url + " match match_pattern_album_page")

        response = Selector(response)
        xpaths = ['//@href', '//@src', '//@data-original']
        for xpath in xpaths:
            page_response = response.xpath(xpath).extract()
            for url in page_response:
                if url.endswith('.jpg') or url.endswith('.png'):
                    album_image = AlbumImage()
                    album_image['url'] = url
                    arr = url.split(r'/')
                    if len(arr) < 3:
                        continue
                    gallery = arr[-4]
                    star_id = arr[-3]
                    album_id = arr[-2]

                    if gallery != "gallery" or not str.isnumeric(star_id) \
                        or not str.isnumeric(album_id):
                        continue

                    album_image['album_id'] = album_id
                    album_image['star_id'] = star_id
                    album_image['type'] = "AlbumImage"
                    self.nvshens_spider.img_all[url] = True
                    yield album_image

        arr = cur_page_url.split(r'/')
        album_id = arr[4] if (len(arr) >= 5) else None
        if album_id is not None:
            try:
                album_name = response.xpath('/html/body/div[2]/h1[@id="htilte"]/text()').extract()
                album_desc = response.xpath('//*[@id="ddesc"]/text()').extract()
                info = response.xpath('//*[@id="dinfo"]/text()').extract()[1]
                publish_date = re.findall("\d{4}\/\d{1,2}\/\d{1,2}", info)[0]
                view_count = re.findall("\d+", re.findall("了 \d+ 次", info)[0])[0]
                company = ""

                album_info = AlbumInfo()
                album_info['album_name'] = album_name
                album_info['publish_date'] = publish_date
                album_info['description'] = album_desc
                album_info['company'] = company
                album_info['album_id'] = album_id
                album_info['type'] = 'AlbumInfo'
                yield album_info
            except Exception as e:
                print(e)

    def parse_star_page(self, response):
        print("in parse_star_page *******************")
        if not self.nvshens_spider.nvshens_url_matcher.\
                match_pattern_star_page(response.url):
            return
        cur_url = response.url

        try:
            response = Selector(response)

            girl_info = self.try_xpath_extract(response,
                            '/html/body/div[@id="wrapper"]'
                            '/div[@id="post"]/div[@class="entry_box"]'
                            '/div[@class="res_infobox clearfix"]'
                            '/div[@class="infodiv"]'
                            '/table/tr/td/text()')
            girl_id = self.try_xpath_extract_first(response, '//input[@id="girlid"]/@value')
            girl_name = self.try_xpath_extract_first(response, '//*[@id="post"]/div/div/div/h1/text()')
            girl_cover = self.try_xpath_extract_first(response, '//*[@id="post"]/div[2]/div/div[3]/a/img/@src')

            girl_description = self.try_xpath_extract_first(response,
                    '/html/body/div[@id="wrapper"]/div[@id="post"]/' 
                    'div[@class="entry_box"]/div[@class="box_entry"]'
                    '/div[@class="box_entry_title"]/div[@class="infocontent"]/p/text()')
            if girl_description is None:
                girl_description = self.try_xpath_extract_first(response,
                    '/html/body/div[@id="wrapper"]/div[@id="post"]/'
                    'div[@class="entry_box"]/div[@class="box_entry"]'
                    '/div[@class="box_entry_title"]/div[@class="infocontent"]/text()')
            if girl_description is not None:
                girl_description = girl_description.strip()

            if girl_id is not None and girl_info is not None:
                if girl_cover is not None:
                    girl_info.append('cover')
                    l = []
                    l.append(girl_cover)
                    girl_info.append(l)

                if girl_description is not None:
                    girl_info.append('description')
                    girl_info.append(girl_description)

                if girl_id is not None:
                    girl_info.append('starId')
                    girl_info.append(girl_id)

                if girl_name is not None:
                    girl_info.append('name')
                    girl_info.append(girl_name)

                info = Info()
                info['info'] = girl_info
                info['type'] = 'Info'
                yield info
        except Exception as e:
            print(e)
            failed_url = FailedURL()
            failed_url['url'] = cur_url
            failed_url['func'] = 'parse_star_page'
            failed_url['type'] = 'FailedURL'
            yield failed_url

        for v in self.parse_star_album_list_page(response):
            yield v

    def parse_star_album_list_page(self, response):
        try:
            xpaths = ['//@href', '//@src', '//@data-original']
            for xpath in xpaths:
                page_response = response.xpath(xpath).extract()
                for url in page_response:
                    print(url)
                    if url.endswith('.jpg') or url.endswith('.png'):
                        if url not in self.nvshens_spider.img_all:
                            album_cover = AlbumCover()
                            album_cover['url'] = url
                            arr = url.split(r'/')
                            if len(arr) < 5:
                                continue
                            gallery = arr[-5]
                            star_id = arr[-4]
                            album_id = arr[-3]
                            cover = arr[-2]

                            if gallery != "gallery" or cover != "cover" or \
                                    not str.isnumeric(star_id) or \
                                    not str.isnumeric(album_id):
                                continue

                            album_cover['album_id'] = album_id
                            album_cover['star_id'] = star_id
                            album_cover['type'] = "AlbumCover"
                            self.nvshens_spider.img_all[url] = True
                            yield album_cover
        except Exception as e:
            print(e)
            failed_url = FailedURL()
            failed_url['url'] = response.url
            failed_url['func'] = 'parse_star_album_list_page'
            failed_url['type'] = 'FailedURL'
            yield failed_url

    def parse_album_tag_page(self, response):
        if not self.nvshens_spider.nvshens_url_matcher.match_pattern_tag_album_page(response.url):
            return

        print("in parse_album_tag_page *******************")
        current_url = response.url
        response = Selector(response)

        try:
            tagNameChn = response.xpath('/html/body/div[@id="wrapper"]/div[@id="post_rank"]'
                '/div[@class="entry_box_arena"]/div[@class="box_entry"]'
                '/div[@class="tag_div"]/ul/li/a[@class="cur_tag_a"]/text()'
                                          ).extract()[0]

            tagNameEng =  parse.urlparse(current_url).path.split('/')[2]
            albumURLs = response.xpath('/html/body/div[@id="wrapper"]/div[@id="post_rank"]'
                '/div[@class="entry_box_arena"]/div[@class="box_entry"]'
                '/div[@class="post_entry"]/div[@id="listdiv"]/ul/li[@class="galleryli"]'
                '/div[@class="galleryli_div"]/a/@href').extract()
        except:
            print('!!!!! error in processing page : ' + current_url)
            return

        albumIDList = []
        for albumURL in albumURLs:
            albumId = albumURL.split('/')[2]
            albumIDList.append(int(albumId))

        tag_page = TagPage()
        tag_page['tagName'] = tagNameChn
        tag_page['tagId'] = tagNameEng
        tag_page['IDList'] = albumIDList
        tag_page['tagTypeId'] = 'Album'
        tag_page['type'] = "TagPage"
        yield tag_page

    def parse_star_tag_page(self, response):
        if not self.nvshens_spider.nvshens_url_matcher.match_pattern_tag_star_page(response.url):
            return

        print("in parse_star_tag_page *******************")
        current_url = response.url
        response = Selector(response)

        tagNameChn = self.try_xpath_extract_first(response,
                        '//*[@id="post_rank"]/div/div/div/ul/li/a[@class="cur_tag_a"]/text()')
        tagNameEng = self.try_get_split_result(current_url, '/', -2)
        starURLs = self.try_xpath_extract(response, '//*[@id="listdiv"]/ul/li/div/a/@href')

        starIDList = []
        for starURL in starURLs:
            starId = self.try_get_split_result(starURL, '/', 2)
            if starId is not None and starId.isdigit():
                starIDList.append(int(starId))

        tag_page = TagPage()
        tag_page['tagName'] = tagNameChn
        tag_page['tagId'] = tagNameEng
        tag_page['IDList'] = starIDList
        tag_page['tagTypeId'] = 'Star'
        tag_page['type'] = "TagPage"
        yield tag_page


class NvshensSpider(Spider):
    nvshens_url_matcher = NvshensURLMatcher()

    name = 'nvshens'
    domain = 'https://www.nvshens.com'
    allowed_domains = ['nvshens.com']
    start_urls = [
        'https://www.nvshens.com/g/16239/',
        'https://www.nvshens.com/girl/21132/album/',
        'https://www.nvshens.com/tag/f90/',
        'https://www.nvshens.com/gallery/oumei/',
        'https://www.nvshens.com/gallery/xinggan/',
        'https://www.nvshens.com/girl/21132/',
        ]

    img_all = {}
    url_all = {}

    url_num_limit = 99999999999999999
    url_num_limit = 2000

    spider_helper = NvshensSpiderHelper()
    extract_url_on = True

    def __init__(self):
        super(Spider).__init__()
        self.spider_helper.nvshens_spider = self

    def parse(self, response):
        self.url_all[response.url] = True
        if len(self.url_all) >= self.url_num_limit:
            return

        page_url = PageUrl()
        page_url['url'] = response.url
        page_url['type'] = "PageUrl"
        yield page_url

        url = response.url
        if self.nvshens_url_matcher.match_pattern_domain(url):
            if self.nvshens_url_matcher.match_pattern_star_page(url):
                print("yield Request(url, callback=self.parse_tag_page)")
                for v in self.spider_helper.parse_star_page(response):
                    yield v
            elif self.nvshens_url_matcher.match_pattern_star_album_list_page(url):
                print("yield Request(url, callback=self.parse_star_album_list_page)")
                for v in self.spider_helper.parse_star_album_list_page(response):
                    yield v
            elif self.nvshens_url_matcher.match_pattern_album_page(url):
                print("yield Request(url, callback=self.parse_album_page)")
                for v in self.spider_helper.parse_album_page(response):
                    yield v
            elif self.nvshens_url_matcher.match_pattern_tag_album_page(url):
                print("yield Request(url, callback=self.parse_album_tag_page)")
                for v in self.spider_helper.parse_album_tag_page(response):
                    yield v
            elif self.nvshens_url_matcher.match_pattern_tag_star_page(url):
                print("yield Request(url, callback=self.parse_star_tag_page)")
                for v in self.spider_helper.parse_star_tag_page(response):
                    yield v
            else:
                no_match_url = NoMatchUrl()
                no_match_url['url'] = url
                no_match_url['type'] = "NoMatchUrl"
                yield no_match_url

            if self.nvshens_url_matcher.match_pattern_extract_page(url):
                print("yield Request(url, callback=self.extract_url)")
                if not self.extract_url_on:
                    return

                link_extractor = LinkExtractor()
                links = link_extractor.extract_links(response)
                for link in links:
                    print("extract_url in for : " + link.url)
                    if self.nvshens_url_matcher.match_pattern_extract_page(link.url) \
                            and link.url not in self.url_all and \
                            len(self.url_all) < self.url_num_limit:
                        self.url_all[link.url] = True
                        print("extract_url : " + link.url)
                        yield Request(link.url, callback=self.parse)
