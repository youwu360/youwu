# -*- coding: utf-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import Info, ImageUrl
from urllib.parse import urljoin
import time
from ..ProxyScrapyer import ProxyScrapyer


class NvshensSpider(Spider):

    proxy_scrapyer = ProxyScrapyer()
    last_run_time = 0
    proxy_list = []

    name = 'nvshens'
    domain = 'https://www.nvshens.com'
    allowed_domains = ['nvshens.com']
    start_urls = [
        'https://www.nvshens.com/girl/22162/',
        'https://www.nvshens.com/g/22808/',
        ]

    url_all = {}
    img_all = {}
    url_num_limit = 100

    def parse(self, response):
        self.update_proxy()

        print("parse ," + response.url)
        response = Selector(response)

        girl_info = response.xpath('/html/body/div[@id="wrapper"]'
                              '/div[@id="post"]/div[@class="entry_box"]'
                              '/div[@class="res_infobox clearfix"]'
                              '/div[@class="infodiv"]'
                              '/table/tr/td/text()').extract()
        girl_id = response.xpath('/html/body/div[@id="wrapper"]'
                                 '/div[@id="post"]/div[@class="entry_box"]'
                                 '/div[@class="res_infobox clearfix"]'
                                 '/input[@id="girlid"]/@value').extract()
        girl_name = response.xpath('/html/body/div[@id="wrapper"]'
                                   '/div[@id="post"]/'
                                   'div[@class="entry_box"]/'
                                   'div[@class="res_infobox clearfix"]'
                                   '/div[@class="div_h1"]'
                                   '/h1[@style="font-size: 15px"]'
                                   '/text()').extract()

        if girl_id is not None and girl_info is not None:
            if type(girl_id) is list and len(girl_id) == 1\
                    and type(girl_name) is list and len(girl_name) == 1:
                girl_info.append(int(girl_id[0]))
                girl_info.append(girl_name[0])

                info = Info()
                info['info'] = girl_info
                yield info

        xpaths = ['//@href', '//@src', '//@data-original']
        for xpath in xpaths:
            page_response = response.xpath(xpath).extract()
            for url in page_response:
                if url.startswith('/'):
                    url = urljoin(self.domain, url)
                if url in self.url_all:
                    continue
                elif url.endswith(".css") or url.endswith('.js') or \
                        url.endswith('aspx'):
                    continue
                elif url.endswith('.jpg') or url.endswith('.png'):
                    if url not in self.img_all:
                        image_url = ImageUrl()
                        image_url['image_url'] = url
                        self.img_all[url] = True
                        yield image_url
                elif url.startswith('http'):
                    if url not in self.url_all and len(self.url_all) <= self.url_num_limit:
                        self.url_all[url] = True
                        yield Request(url, callback=self.parse)

    def update_proxy(self, proxy_time_out=30):
        now = time.time()
        if now - self.last_run_time > proxy_time_out:
            print("proxy_list old :" + ",".join(self.proxy_list))
            self.proxy_list = self.proxy_scrapyer.get_alive_proxy_list()
            print("proxy_list new :" + ",".join(self.proxy_list))
            self.last_run_time = now

