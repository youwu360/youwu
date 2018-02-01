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


class LoadNvshensData():
    lineNum = 0
    lineNumLimit = 11000000000
    # lineNumLimit = 10000

    path = os.path.dirname(os.path.realpath(__file__))
    items_json = os.path.join(path, "items.json")

    pattern_star_cover = re.compile("https://img\.onvshen\.com:85/girl/\d+\/\d+(_s)?\.jpg")
    pattern_album_cover = re.compile("https://img\.onvshen\.com:85/gallery/\d+/\d+/cover/[0-9]+\.jpg")
    pattern_album_image = re.compile("https://img\.onvshen\.com:85/gallery/\d+/\d+(/s/)?/\d+\.jpg")

    starCover = {}
    albumCover = {}
    albumToStar = {}
    albumImageList = {}

    def __init__(self):
        assert self.pattern_star_cover.match("https://img.onvshen.com:85/girl/22100/22100.jpg")
        assert self.pattern_star_cover.match("https://img.onvshen.com:85/girl/22100/22100_s.jpg")
        assert self.pattern_album_cover.match("https://img.onvshen.com:85/gallery/22100/18017/cover/0.jpg")
        assert self.pattern_album_cover.match("https://img.onvshen.com:85/gallery/23391/22100/cover/0.jpg")
        assert self.pattern_album_image.match("https://img.onvshen.com:85/gallery/22100/18017/015.jpg")

    def get_value_by_tag(self, line, tag):
        try:
            for i in range(0, len(line)):
                if tag == line[i]:
                    return line[i + 1]
        except Exception as e:
            print(e)
            print(line)
        return None

    def load_data(self):
        file_read = open(self.items_json, 'r', encoding="utf-8")
        for line in file_read:
            if self.lineNum <= self.lineNumLimit:
                self.lineNum += 1
            else:
                break

            if len(line) <= 10:
                continue
            line = line.strip().strip(",")
            data = json.loads(line)

            if 'type' not in data:
                print("error : do not have type !  ---  ")
                print(data)

            if data['type'] == 'Info':
                info = data['info']
                cover = self.get_value_by_tag(info, 'cover')
                if type(cover) is list and len(cover) == 1:
                    cover = cover[0]
                else:
                    cover = None

                try:
                    star_id = int(self.get_value_by_tag(info, 'starId'))
                    self.starCover[star_id] = cover
                except Exception as e:
                    print(e)
                    print(info)
            elif data['type'] == 'AlbumCover':
                url = data['url']
                star_id = int(data['star_id'])
                album_id = int(data['album_id'])
                self.albumToStar[album_id] = star_id
                self.albumCover[album_id] = url
            elif data['type'] == 'AlbumImage':
                url = data['url']
                star_id = int(data['star_id'])
                album_id = int(data['album_id'])
                self.albumToStar[album_id] = star_id
                if album_id not in self.albumImageList:
                    self.albumImageList[album_id] = {}
                try:
                    self.albumImageList[album_id][url.split('/')[-1]] = url
                except Exception as e:
                    print(e)
                    print(url)
                    print(data)
    def save(self, target='all_image_urls.json'):
        res = {}
        res['starCover'] = self.starCover
        res['albumCover'] = self.albumCover
        res['albumToStar'] = self.albumToStar
        res['albumImageList'] = self.albumImageList
        with open(target, 'w') as fp:
            json.dump(res, fp)
    def run(self):
        self.load_data()
        self.save()

if __name__ == '__main__':
    loader = LoadNvshensData()
    loader.run()
