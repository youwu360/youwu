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
    star_id_start = 0
    star_id_end = 999999999999

    path = os.path.dirname(os.path.realpath(__file__))
    items_json = os.path.join(path,
                              "../spider/spider_nvshens/myproject/items.json")

    pattern_star_cover = re.compile("https://img\.onvshen\.com:85/girl/\d+\/\d+(_s)?\.jpg")
    pattern_album_cover = re.compile("https://img\.onvshen\.com:85/gallery/\d+/\d+/cover/[0-9]+\.jpg")
    pattern_album_image = re.compile("https://img\.onvshen\.com:85/gallery/\d+/\d+(/s/)?/\d+\.jpg")

    starCover = {}
    starInfo = {}
    albumInfos = {}
    starAlbum = {}
    starAlbumCover = {}
    albumToStar = {}
    album_tag_id_to_name = {}
    album_tag_id_to_list = {}
    star_tag_id_to_name = {}
    star_tag_id_to_list = {}
    noMatchData = []

    info_key = 'info'
    image_url_key = 'image_url'

    def __init__(self):
        assert self.pattern_star_cover.match("https://img.onvshen.com:85/girl/22100/22100.jpg")
        assert self.pattern_star_cover.match("https://img.onvshen.com:85/girl/22100/22100_s.jpg")
        assert self.pattern_album_cover.match("https://img.onvshen.com:85/gallery/22100/18017/cover/0.jpg")
        assert self.pattern_album_cover.match("https://img.onvshen.com:85/gallery/23391/22100/cover/0.jpg")
        assert self.pattern_album_image.match("https://img.onvshen.com:85/gallery/22100/18017/015.jpg")

        Star.objects.all().delete()
        Album.objects.all().delete()
        Tags.objects.all().delete()

    def load_data_to_memory(self):
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
                try:
                    info = data[self.info_key]
                    info = self.parse_star(info)
                    if 'starId' in info:
                        self.starInfo[info['starId']] = info
                except:
                    print("error in parse : " + json.dumps(data[self.info_key]))

            elif data['type'] == 'AlbumCover':
                url = data['url']
                star_id = data['star_id']
                album_id = data['album_id']
                self.albumToStar[album_id] = star_id
                self.append_album_cover(album_id, url)
            elif data['type'] == 'AlbumImage':
                url = data['url']
                star_id = data['star_id']
                album_id = data['album_id']
                self.albumToStar[album_id] = star_id
                self.append_album(album_id, url)
            elif data['type'] == 'TagPage' and data['tagTypeId'] == 'Album':
                tag_id = data['tagId']
                tag_name = data['tagName']
                id_list = data['IDList']

                self.album_tag_id_to_name[tag_id] = tag_name
                if tag_id in self.album_tag_id_to_list:
                    self.album_tag_id_to_list[tag_id] = self.album_tag_id_to_list[tag_id]\
                                                        + id_list
                else:
                    self.album_tag_id_to_list[tag_id] = id_list
            elif data['type'] == 'TagPage' and data['tagTypeId'] == 'Star':
                tag_id = data['tagId']
                tag_name = data['tagName']
                id_list = data['IDList']

                self.star_tag_id_to_name[tag_id] = tag_name
                if tag_id in self.star_tag_id_to_list:
                    self.star_tag_id_to_list[tag_id] = self.star_tag_id_to_list[tag_id] + id_list
                else:
                    self.star_tag_id_to_list[tag_id] = id_list
            elif data['type'] == "AlbumInfo":
                album_id = data['album_id']
                self.albumInfos[album_id] = data
            else:
                self.noMatchData.append(data)

    def insert_tags_to_db(self):
        for tagId in self.star_tag_id_to_name:
            tag = {}
            tagName = self.star_tag_id_to_name[tagId]
            IDList = json.dumps(self.star_tag_id_to_list[tagId])
            tag['tagId'] = tagId
            tag['tagName'] = tagName
            tag['IdList'] = IDList
            tag['tagTypeId'] = 'Star'
            insert_tags(tag)

        for tagId in self.album_tag_id_to_name:
            tag = {}
            tagName = self.album_tag_id_to_name[tagId]
            IDList = json.dumps(self.album_tag_id_to_list[tagId])
            tag['tagId'] = tagId
            tag['tagName'] = tagName
            tag['IdList'] = IDList
            tag['tagTypeId'] = 'Album'
            insert_tags(tag)

    def insert_stars_to_db(self):
        for star_id in self.starInfo.keys():
            if star_id is None or int(star_id) > self.star_id_end or \
                    int(star_id) < self.star_id_start:
                continue
            star_info = self.starInfo[star_id]

            res = Tags.objects.filter(tagTypeId='Star')
            tags = []
            for v in res:
                id_list = json.loads(v.IdList)
                if int(star_id) in id_list:
                    tags.append(v.tagId)

            star_info['tag'] = json.dumps(tags)
            insert_star(star_info)

    def insert_albums_to_db(self):
        for album_id in self.starAlbum.keys():
            star_id = 0
            if album_id in self.albumToStar:
                star_id = self.albumToStar[album_id]
            if int(star_id) > self.star_id_end or int(star_id) < self.star_id_start:
                continue

            album_path = os.path.join(self.path, "../youwu-resource/data/url_info/" +
                                      str(star_id) + "." + str(album_id))
            album_path = os.path.abspath(album_path)
            with open(album_path, 'w') as outfile:
                json.dump(self.starAlbum[album_id], outfile)

            album_info = {}

            if album_id in self.albumToStar:
                album_info['starId'] = self.albumToStar[album_id]
            else:
                album_info['starId'] = 0

            album_info['albumId'] = album_id

            album_info['cover'] = ''
            if album_id in self.starAlbumCover:
                print('album cover exists, albumId : ' + str(album_id))
                album_info['cover'] = json.dumps(self.starAlbumCover[album_id])
            else:
                print('album cover not exists, albumId : ' + str(album_id))

            album_info['imageListFile'] = album_path
            album_info['pictureCnt'] = len(self.starAlbum[album_id])
            if album_id in self.albumInfos:
                album_info['company'] = self.albumInfos[album_id]['company']
                album_info['Description'] = self.albumInfos[album_id]['description']
                album_info['Name'] = self.albumInfos[album_id]["album_name"]
                album_info['publishDate'] = self.albumInfos[album_id]["publish_date"]
            else:
                album_info['company'] = None
                album_info['Description'] = None
                album_info['Name'] = None
                album_info['publishDate'] = None

            res = Tags.objects.filter(tagTypeId='Album')
            tags = []
            for v in res:
                id_list = json.loads(v.IdList)
                if int(album_id) in id_list:
                    tags.append(v.tagId)

            album_info['tag'] = json.dumps(tags)
            insert_album(album_info)

    def destruct(self):
        with open('noMatchUrl.json', 'w') as outfile:
            json.dump(self.noMatchData, outfile)

        with open('starAlbumCover.json', 'w') as outfile:
            json.dump(self.starAlbumCover, outfile)

        with open('starAlbum.json', 'w') as outfile:
            json.dump(self.starAlbum, outfile)

        with open('starCover.json', 'w') as outfile:
            json.dump(self.starCover, outfile)

    def append_star_cover(self, star_id, url):
        self.append(self.starCover, star_id, url)

    def append_album_cover(self, album_id, url):
        self.append(self.starAlbumCover, album_id, url)

    def append_album(self, album_id, url):
        self.append(self.starAlbum, album_id, url)

    def append(self, to, id, url):
        if id not in to:
            to[id] = []
        if url not in to[id]:
            to[id].append(url)

    def get_value_by_tag(self, line, tag):
        for i in range(0, len(line), 2):
            if tag == line[i]:
                return line[i + 1]
        return None

    def parse_star(self, line):
        if type(line) is not list or len(line) < 5:
            return None
        info = {}
        info['starId'] = self.get_value_by_tag(line, 'starId')
        info['name'] = self.get_value_by_tag(line, 'name')
        info['cover'] = json.dumps(self.get_value_by_tag(line, 'cover'))
        info['birthday'] = self.get_value_by_tag(line, '生 日：')
        info['threeD'] = self.get_value_by_tag(line, '三 围：')
        info['height'] = self.get_value_by_tag(line, '身 高：')
        weight_str = self.get_value_by_tag(line, '体 重：')
        if weight_str is not None:
            weight_data = weight_str.split(" ")
            info['weight'] = float(weight_data[0])
        else:
            info['weight'] = -1

        info['hobby'] = self.get_value_by_tag(line, '兴 趣：')
        info['birthPlace'] = self.get_value_by_tag(line, '出 生：')
        info['description'] = self.get_value_by_tag(line, 'description')

        return info


if __name__ == '__main__':
    loader = LoadNvshensData()
    loader.load_data_to_memory()
    loader.insert_tags_to_db()
    loader.insert_stars_to_db()
    loader.insert_albums_to_db()
