# -*- coding: utf-8 -*-

import json
import os.path
import threading
import time
import urllib.request
from urllib.request import build_opener, ProxyHandler
from scrapy import Selector
from selenium import webdriver


class ProxyScrapyer(object):
    def __init__(self):
        self.proxyFile = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                      'proxyFile.txt')
        self.testUrl = "https://www.nvshens.com/gallery/tgod/"
        self.threads = 50
        self.timeout = 3
        self.alive_proxy = set()
        self.current_page = 0
        self.page_limit = 10

    def run(self):
        self.get_local_proxy()

        for i in range(1, self.page_limit + 1):
            t = threading.Thread(target=self.get_alive_proxy_list_in_one_page, args=(i,))
            t.setDaemon(True)
            t.start()
            time.sleep(10)

        pre_alive_proxy_count = len(self.alive_proxy)
        i = 0
        while i < 60:
            i += 1
            cur_alive_proxy_count = len(self.alive_proxy)
            if cur_alive_proxy_count != pre_alive_proxy_count:
                i = 0
                time.sleep(1)

        self.save_alive_proxy_to_file()
        print("total alive proxy count : " + str(len(self.alive_proxy)))

    def get_alive_proxy_list_in_one_page(self, page_num):
        try:
            t = threading.Thread(target=self.get_alive_proxy_list, args=(page_num,))
            t.setDaemon(True)
            t.start()
            t.join(timeout=100)
            if t.is_alive():
                t._stop()
        except:
            print("page num : " + str(page_num) + " stoped with exception ! ")

    def get_alive_proxy_list(self, page_num):
        proxy_list = self.get_free_proxy_from_daili(page_num)
        for proxy in proxy_list:
            while threading.active_count() > self.threads:
                time.sleep(0.1)
            t = threading.Thread(target=self.link_with_proxy, args=(proxy,))
            t.setDaemon(True)
            t.start()

    def save_alive_proxy_to_file(self):
        with open(self.proxyFile, 'w') as fp:
            json.dump(list(self.alive_proxy), fp)

    def get_local_proxy(self):
        if os.path.exists(self.proxyFile):
            with open(self.proxyFile, 'r', encoding='utf-8') as fp:
                content = fp.read()
                if content:
                    proxy_list = json.loads(content, encoding='utf-8')
                    for proxy in proxy_list:
                        self.link_with_proxy(proxy)
                else:
                    print(self.proxyFile + " is null ! ")

    def link_multi_thread(self, proxy):
        server = "http://" + proxy
        proxy_handler = ProxyHandler({'http': server})
        opener = build_opener(proxy_handler)
        try:
            urllib.request.install_opener(opener)
            req = urllib.request.Request(self.testUrl)
            sock = urllib.request.urlopen(req)
            assert sock.read() is not None
        except:
            if proxy in self.alive_proxy:
                self.alive_proxy.remove(proxy)
            print(proxy + " is unavailable ! ")
            return
        self.alive_proxy.add(proxy)
        print(proxy + " is available ! ")

    def link_with_proxy(self, proxy):
        try:
            t = threading.Thread(target=self.link_multi_thread, args=(proxy,))
            t.setDaemon(True)
            t.start()
        except Exception as e:
            print("parameter proxy : " + str(proxy))
            print(e)

    def get_free_proxy_from_daili(self, page_num, url="http://www.kuaidaili.com/free/inha/"):
        url += str(page_num) + "/"
        print("processing page :" + url)
        free_proxy_list = []
        browser = webdriver.PhantomJS()

        browser.set_page_load_timeout(20)
        try:
            browser.get(url)
        except:
            pass

        for i in range(60):
            html = browser.page_source
            if html is None or len(html) < 15000:
                time.sleep(1)
            else:
                break
        time.sleep(3)

        selector = Selector(text=browser.page_source)
        ips = selector.xpath('//td[@data-title="IP"]/text()').extract()
        ports = selector.xpath('//td[@data-title="PORT"]/text()').extract()

        if len(ips) != len(ports):
            print("error in processing ip and port !")
        for i in range(len(ips)):
            free_proxy_list.append(str(ips[i]) + ":" + str(ports[i]))
        browser.close()
        return free_proxy_list

    def get_local_html_content(self):
        fp = open("../../kuaidaili.html", 'r', encoding='utf-8')
        context = fp.readlines()
        print(type(context))
        print(context)
        print(len(context))
        print(len("".join(context)))


if __name__ == '__main__':
    instance = ProxyScrapyer()
    instance.run()

