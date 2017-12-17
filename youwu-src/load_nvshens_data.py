# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "basics.settings")
import django
import re
import time


django.setup()

import json
import random

from load_nvshens_helper import insert_star, parse_star, insert_album

path = os.path.dirname(os.path.realpath(__file__))
items_json = os.path.join(path, "../youwu-resource/data/text/items.json")

file_object = open(items_json, 'r', encoding="utf-8")

info_key = 'info'
image_url_key = 'image_url'


pattern_star_cover = re.compile("[\w\d:\/\.]+\/girl\/\d+\/\d+\.jpg$")
pattern_star_cover_s = re.compile("[\w\d:\/\.]+\/girl\/\d+\/\d+_s\.jpg$")
pattern_album_cover = re.compile("[\w\d:\/\.]+/gallery/\d+/\d+/cover/[0-9]+\.jpg")
pattern_album_image = re.compile("[\w\d:\/\.]+/gallery/\d+/\d+/\d+\.jpg")
pattern_album_image_s = re.compile("[\w\d:\/\.]+/gallery/\d+/\d+/s/\d+\.jpg")

starCover = {}
starInfo = {}
starAlbum = {}
starAlbumCover = {}
albumToStar = {}

noMatchUrl = []


def append_star_cover(star_id, url):
    global starCover
    append(starCover, star_id, url)


def append_album_cover(album_id, url):
    global starAlbumCover
    append(starAlbumCover, album_id, url)


def append_album(album_id, url):
    global starAlbum
    append(starAlbum, album_id, url)


def append(to, id, url):
    if id not in to:
        to[id] = []
    to[id].append(url)


lineNum = 0
lineNumLimit = 20000000

star_id_start= 22000
star_id_end = 22200

for line in file_object:

    if lineNum <= lineNumLimit:
        lineNum += 1
    else:
        break

    if len(line) <= 10:
        continue
    line = line.strip().strip(",")
    data = json.loads(line)

    if info_key in data:
        try:
            info = data[info_key]
            info = parse_star(info)
            if 'starId' not in info:
                continue
            starInfo[info['starId']] = info
        except:
            print("error in parse : " + json.dumps(data[info_key]))
    elif image_url_key in data:
        image_url = data[image_url_key]
        if pattern_star_cover.match(image_url) or \
                pattern_star_cover_s.match(image_url):
            try:
                star_id = re.search(r'(\d+)', image_url[re.search('girl', image_url).span()[1]:]).group()
                if star_id is not None:
                    append_star_cover(star_id, image_url)
            except:
                print("pattern_star_cover fail : " + image_url)
        elif pattern_album_cover.match(image_url):
            try:
                gallary_search = re.search('gallery', image_url)
                gallary_end = gallary_search.span()[1]
                star_id_search = re.search(r'(\d+)', image_url[gallary_search.span()[1]:])
                star_id = star_id_search.group()
                album_id_search = re.search(r'(\d+)', image_url[gallary_end + star_id_search.span()[1]:])
                album_id = album_id_search.group()
                albumToStar[album_id] = star_id
                append_album_cover(album_id, image_url)
            except:
                print("pattern_album_cover fail : " + image_url)
        elif pattern_album_image.match(image_url) or \
                pattern_album_image_s.match(image_url):
            try:

                gallary_search = re.search('gallery', image_url)
                gallary_end = gallary_search.span()[1]
                star_id_search = re.search(r'(\d+)', image_url[gallary_search.span()[1]:])
                star_id = star_id_search.group()
                album_id_search = re.search(r'(\d+)', image_url[gallary_end + star_id_search.span()[1]:])
                album_id = album_id_search.group()

                albumToStar[album_id] = star_id
                append_album(album_id, image_url)
            except:
                print("pattern_album_image fail : " + image_url)
        else:
            noMatchUrl.append(image_url)


for star_id in starInfo.keys():
    if int(star_id) > star_id_end or int(star_id) < star_id_start:
        continue
    star_info = starInfo[star_id]
    star_info['cover'] = ''
    if star_id in starCover:
        star_info['cover'] = json.dumps(starCover[star_id])
        print('star cover exists, starId : ' + str(star_id))
    else:
        print('star cover not exists, starId : ' + str(star_id))
    insert_star(star_info)

for album_id in starAlbum.keys():
    star_id = 0
    if album_id in albumToStar:
        star_id = albumToStar[album_id]
    if int(star_id) > star_id_end or int(star_id) < star_id_start:
        continue

    album_path = os.path.join(path, "../youwu-resource/data/url_info/" + str(star_id) + "." + str(album_id))
    album_path = os.path.abspath(album_path)
    with open(album_path, 'w') as outfile:
        json.dump(starAlbum[album_id], outfile)

    album_info = {}

    if album_id in albumToStar:
        album_info['starId'] = albumToStar[album_id]
    else:
        album_info['starId'] = 0

    album_info['albumId'] = album_id

    album_info['cover'] = ''
    if album_id in starAlbumCover:
        print('album cover exists, albumId : ' + str(album_id))
        album_info['cover'] = json.dumps(starAlbumCover[album_id])
    else:
        print('album cover not exists, albumId : ' + str(album_id))
    album_info['imageListFile'] = album_path
    album_info['pictureCnt'] = len(starAlbum[album_id])
    insert_album(album_info)

print(starAlbum)
print(starAlbumCover.keys())

with open('noMatchUrl.json', 'w') as outfile:
    json.dump(noMatchUrl, outfile)

