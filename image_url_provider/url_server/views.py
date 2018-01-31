from django.shortcuts import render
from django.http import HttpResponse
import json
import os
import hashlib

# Create your views here.

def cover_url(request, starId, albumId):
    basePath = os.path.dirname(os.path.realpath(__file__))
    jsonDataPath = os.path.abspath(os.path.join(basePath,
                    "../../spider/spider_nvshens/scrapy_album_image_to_local/data"))
    jsonDataSubPath = os.path.join(jsonDataPath, hashlib.md5((str(starId) + "-" + str(albumId)).encode('utf-8')).hexdigest()[0:2])

    jsonFilePath = os.path.join(jsonDataSubPath, str(starId) + "." + str(albumId) + ".json")
    fp = open(jsonFilePath)
    res = json.load(fp)
    return HttpResponse(json.dumps(res))
