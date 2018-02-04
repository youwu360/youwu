# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "basics.settings")
import django
import re
import time
django.setup()
import json
import random
from site_youwu.models import Star, Album, Tags
from load_nvshens_helper import insert_star, insert_album, insert_tags
import datetime


allUrlsForProductInJsonFile = '/tmp/allUrlsForProduct.json'
allUrlsForProductInJson = None
if os.path.exists(allUrlsForProductInJsonFile):
    allUrlsForProductInJson = json.load(open(allUrlsForProductInJsonFile))

starCover = 'starCover'
albumCover = 'albumCover'
albumToStar = 'albumToStar'
albumImageList = 'albumImageList'



class LoadNewCover:

    def loadStarCover(self):
        for starId in allUrlsForProductInJson[starCover]:
            url = allUrlsForProductInJson[starCover][starId]
            try:
                if Album.objects.filter(starId=starId).exists():
                    v = Star.objects.get(starId=starId)
                    v.cover = json.dumps([url])
                    v.save()
                    print("updated starId : " + str(starId))
                else:
                    print("updated starId failed , starId not exists : " + str(starId))
            except Exception as e:
                print("try update fail in updated star")
                print(e)

    def loadAlbumCover(self):
        for albumId in allUrlsForProductInJson[albumCover]:
            url = allUrlsForProductInJson[albumCover][albumId]
            try:
                if Album.objects.filter(albumId=albumId).exists():
                    v = Album.objects.get(albumId=albumId)
                    v.cover = json.dumps([url])
                    v.save()
                    print("updated albumId : " + str(albumId))
            except Exception as e:
                print("try update fail in updated album")
                print(e)

if __name__ == '__main__':
    loader = LoadNewCover()
    loader.loadStarCover()
    loader.loadAlbumCover()
