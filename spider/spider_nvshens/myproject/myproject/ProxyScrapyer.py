# -*- coding: utf-8 -*-

import re
import threading
from scrapy import Selector
import time
from selenium import webdriver
import json
import os.path
from urllib.request import build_opener, ProxyHandler, URLError
import urllib.request


class ProxyScrapyer(object):
    def __init__(self):
        self.proxyFile = 'proxyFile.txt'
        self.testUrl = "https://www.baidu.com"
        self.threads = 5
        self.timeout = 3
        self.regex = re.compile(r'baid.com')
        self.aliveProxyList = []

    def get_alive_proxy_list(self):
        self.update_alive_proxy_list()
        return self.aliveProxyList;

    def update_alive_proxy_list(self):
        proxy_list = self.get_proxy_list()
        proxy_list = list(set(proxy_list))
        self.aliveProxyList.clear()
        for proxy in proxy_list:
            if threading.active_count() > self.threads:
                time.sleep(1)
                continue
            else:
                t = threading.Thread(target=self.link_with_proxy, args={proxy, })
                t.start()

        while threading.active_count() > 1:
            print("remaining thread count : " + str(threading.active_count()))
            time.sleep(1)

    def get_alive_proxy_and_save_to_file(self):
        alive_proxy = self.get_alive_proxy_list()
        with open(self.proxyFile, 'w') as fp:
            json.dump(alive_proxy, fp)

    def get_proxy_list(self):
        local_proxy = self.get_local_proxy()
        online_proxy = self.get_free_proxy_from_kuaidaili()
        return local_proxy + online_proxy + self.aliveProxyList

    def get_local_proxy(self):
        if os.path.exists(self.proxyFile):
            with open(self.proxyFile, 'r', encoding='utf-8') as fp:
                content = fp.read()
                if content:
                    print(self.proxyFile + " is not null ")
                    print('content :')
                    print(content)
                    proxy_list = json.loads(content, encoding='utf-8')
                    return proxy_list
                else:
                    print(self.proxyFile + " is null ! ")
        return []

    def link_with_proxy(self, proxy):
        server = "http://" + proxy
        proxy_handler = ProxyHandler({'http' : server})
        opener = build_opener(proxy_handler)
        try:
            urllib.request.install_opener(opener)
            urllib.request.urlopen(self.testUrl)
            self.aliveProxyList.append(proxy)
            print(proxy + " is available ! ")
        except:
            print(proxy + " is unavailable ! ")

    def get_free_proxy_from_kuaidaili(self):
        free_proxy_list = []
        api = "http://www.kuaidaili.com/free/"
        browser = webdriver.Firefox()
        browser.set_page_load_timeout(20)
        browser.get(api)

        for i in range(60):
            html = browser.page_source
            if html is None or len(html) < 15000:
                time.sleep(1)
            else:
                break

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
    instance.get_alive_proxy_and_save_to_file()

