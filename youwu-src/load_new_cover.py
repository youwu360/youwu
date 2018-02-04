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


allUrlsForProductInJsonFile = 'allUrlsForProduct.json'
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
                if Star.objects.filter(starId=starId).exists():
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

class CleanNullAlbum:

    toSave = {}
    toDelete = {}
    def __init__(self):
        albumIdToList = {}
        if albumImageList in allUrlsForProductInJson:
            albumIdToList = allUrlsForProductInJson[albumImageList]

        for albumId in albumIdToList:
            imgList = albumIdToList[albumId]
            if len(imgList) > 0:
                self.toSave[albumId] = True
            else:
                self.toDelete[albumId] = True

    def delete_album(self):

        albums = Album.objects.all()

        cnt = 0
        for album in albums:
            albumId = str(album.albumId)
            if albumId in self.toSave:
                continue

            cnt += 1
            print("album.delete()")
            print(album.albumId)
            print("cnt: " + str(cnt))

        print(len(self.toSave))
        print(len(self.toDelete))

        # for albumId in allUrlsForProductInJson[albumCover]:
        #     url = allUrlsForProductInJson[albumCover][albumId]
        #     try:
        #         if Album.objects.filter(albumId=albumId).exists():
        #             v = Album.objects.get(albumId=albumId)
        #             v.cover = json.dumps([url])
        #             v.save()
        #             print("updated albumId : " + str(albumId))
        #     except Exception as e:
        #         print("try update fail in updated album")
        #         print(e)


if __name__ == '__main__':
    cleaner = CleanNullAlbum()
    cleaner.delete_album()
