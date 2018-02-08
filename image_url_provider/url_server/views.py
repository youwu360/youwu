from django.shortcuts import render
from django.http import HttpResponse
import json
import os
import hashlib

# Create your views here.

def get_all_urls(starId, albumId):
    basePath = os.path.dirname(os.path.realpath(__file__))
    jsonDataPath = os.path.abspath(os.path.join(basePath,
                    "../../spider/spider_nvshens/scrapy_album_image_to_local/data"))
    jsonDataSubPath = os.path.join(jsonDataPath, hashlib.md5((str(starId) + "-" + str(albumId)).encode('utf-8')).hexdigest()[0:2])

    jsonFilePath = os.path.join(jsonDataSubPath, str(starId) + "." + str(albumId) + ".json")

    if not os.path.exists(jsonFilePath):
        return {}
    try:
        fp = open(jsonFilePath)
        res = json.load(fp)
        fp.close()
        return res
    except:
        pass
    return {}

def cover_url(request, starId, albumId):
    urls = get_all_urls(starId, albumId)
    return HttpResponse(json.dumps([urls['cover.jpg']]))

def list_url(request, starId, albumId):
    urls = get_all_urls(starId, albumId)
    res = []
    for k in urls:
        if k != 'cover.jpg':
            res.append(urls[k])
    return HttpResponse(json.dumps(res))