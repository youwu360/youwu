#!/usr/bin/env python
from selenium import webdriver

browser = webdriver.PhantomJS()
browser.get('http://localhost:8000')

print(browser.title)
assert 'Django' in browser.title
