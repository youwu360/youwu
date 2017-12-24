# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "basics.settings")
import django
import re
import time
django.setup()
import json
import random
from load_nvshens_helper import insert_tags



path = os.path.dirname(os.path.realpath(__file__))
tags_json = os.path.join(path, "../spider/spider_nvshens/myproject/tags.json")

page_tag_list = json.load(open(tags_json, 'r', encoding='utf-8'))


tag_id_to_name = {}
tag_id_to_album = {}

for page_tag in page_tag_list:
    tag_id = page_tag['tagId']
    tag_name = page_tag['tagName']
    album_id_list = page_tag['albumIDList']

    tag_id_to_name[tag_id] = tag_name
    if tag_id in tag_id_to_album:
        tag_id_to_album[tag_id] = tag_id_to_album[tag_id] + album_id_list
    else:
        tag_id_to_album[tag_id] = album_id_list


for k in tag_id_to_name:
    tag = {}
    tagId = k
    tagName = tag_id_to_name[tagId]
    albumIDList = json.dumps(tag_id_to_album[tagId])

    tag['tagId'] = tagId
    tag['tagName'] = tagName
    tag['albumIdList'] = albumIDList

    insert_tags(tag)
