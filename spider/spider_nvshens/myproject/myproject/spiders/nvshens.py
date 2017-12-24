# -*- coding: utf-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import Info, ImageUrl, PageUrl, TagPage
from urllib.parse import urljoin
import time
from ..ProxyScrapyer import ProxyScrapyer
from .nvshens_url_match import NvshensURLMatcher
from scrapy.linkextractors import LinkExtractor
from urllib import parse

class NvshensSpider(Spider):
    nvshens_url_matcher = NvshensURLMatcher()

    proxy_scrapyer = ProxyScrapyer()
    last_run_time = 0
    proxy_list = []

    name = 'nvshens'
    domain = 'https://www.nvshens.com'
    allowed_domains = ['nvshens.com']
    start_urls = [
        'https://www.nvshens.com/gallery/oumei/',
        'https://www.nvshens.com/gallery/xinggan/',
        ]

    url_all = {}
    img_all = {}
    url_num_limit = 20000

    parse_album_page_on = False
    parse_star_page_on = False
    parse_tag_page_on = True

    def parse(self, response):
        linkExtractor = LinkExtractor()
        links = linkExtractor.extract_links(response)
        for link in links:
            url = link.url
            print("==================== url : " + url)
            if self.nvshens_url_matcher.match_pattern_domain(url):

                if self.nvshens_url_matcher.match_pattern_star_page(url):
                    print("yield Request(url, callback=self.parse_tag_page)")
                    yield Request(url, callback=self.parse_star_page)
                elif self.nvshens_url_matcher.match_pattern_album_page(url):
                    print("yield Request(url, callback=self.parse_album_page)")
                    yield Request(url, callback=self.parse_album_page)
                elif self.nvshens_url_matcher.match_pattern_tag_page(url):
                    print("yield Request(url, callback=self.parse_tag_page)")
                    yield Request(url, callback=self.parse_tag_page)

                print("yield Request(url, callback=self.extract_url)")
                yield Request(url, callback=self.extract_url)

    def parse_album_page(self, response):
        if not self.parse_album_page_on:
            return

        print("in parse_album_page *******************")
        if not self.nvshens_url_matcher.match_pattern_album_page(response.url):
            return
        response = Selector(response)
        xpaths = ['//@href', '//@src', '//@data-original']
        for xpath in xpaths:
            page_response = response.xpath(xpath).extract()
            for url in page_response:
                if url.endswith('.jpg') or url.endswith('.png'):
                    if url not in self.img_all:
                        image_url = ImageUrl()
                        image_url['image_url'] = url
                        self.img_all[url] = True
                        yield image_url

    def parse_star_page(self, response):
        if not self.parse_star_page_on:
            return
        print("in parse_star_page *******************")
        if not self.nvshens_url_matcher.match_pattern_star_page(response.url):
            return
        response = Selector(response)
        girl_info = response.xpath('/html/body/div[@id="wrapper"]'
                                   '/div[@id="post"]/div[@class="entry_box"]'
                                   '/div[@class="res_infobox clearfix"]'
                                   '/div[@class="infodiv"]'
                                   '/table/tr/td/text()').extract()
        girl_id = response.xpath('/html/body/div[@id="wrapper"]'
                                 '/div[@id="post"]/div[@class="entry_box"]'
                                 '/div[@class="res_infobox clearfix"]'
                                 '/input[@id="girlid"]/@value').extract()[0]
        girl_name = response.xpath('/html/body/div[@id="wrapper"]'
                                   '/div[@id="post"]/'
                                   'div[@class="entry_box"]/'
                                   'div[@class="res_infobox clearfix"]'
                                   '/div[@class="div_h1"]'
                                   '/h1[@style="font-size: 15px"]'
                                   '/text()').extract()[0]
        girl_cover = response.xpath('/html/body/div[@id="wrapper"]'
                                   '/div[@id="post"]'
                                   '/div[@class="entry_box"]'
                                   '/div[@class="res_infobox clearfix"]'
                                   '/div[@class="infoleft_imgdiv"]'
                                   '/a[@class="imglink"]/img/@src'
                                   ).extract()[0]
        girl_description = response.xpath('/html/body/div[@id="wrapper"]/div[@id="post"]/'
                'div[@class="entry_box"]/div[@class="box_entry"]'
                '/div[@class="box_entry_title"]/div[@class="infocontent"]/p/text()'
                                          ).extract()[0]

        if girl_id is not None and girl_info is not None:
            if girl_cover is not None:
                girl_info.append('cover')
                girl_info.append(girl_cover)

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
            yield info

    def extract_url(self, response):
        linkExtractor = LinkExtractor()
        links = linkExtractor.extract_links(response)
        for link in links:

            print("extract_url in for : " + link.url)
            print("len(self.url_all) : " + str(len(self.url_all)))
            if self.nvshens_url_matcher.match_pattern_tag_page(link.url) and \
                    link.url not in self.url_all and \
                    len(self.url_all) < self.url_num_limit:
                self.url_all[link.url] = True
                print("extract_url in ifif : " + link.url)
                yield Request(link.url, callback=self.parse)

    def parse_tag_page(self, response):

        if not self.parse_tag_page_on:
            return
        if not self.nvshens_url_matcher.match_pattern_tag_page(response.url):
            return

        print("in parse_tag_page *******************")
        current_url = response.url
        response = Selector(response)

        try:
            tagNameChn = response.xpath('/html/body/div[@id="wrapper"]/div[@id="post_rank"]'
                '/div[@class="entry_box_arena"]/div[@class="box_entry"]'
                '/div[@class="box_entry_title"]/div[@class="hot_tag"]/span[@id="stag"]/text()'
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
        tag_page['albumIDList'] = albumIDList
        yield tag_page

    def update_proxy(self, proxy_time_out=30):
        now = time.time()
        if now - self.last_run_time > proxy_time_out:
            print("proxy_list old :" + ",".join(self.proxy_list))
            self.proxy_list = self.proxy_scrapyer.get_alive_proxy_list()
            print("proxy_list new :" + ",".join(self.proxy_list))
            self.last_run_time = now

