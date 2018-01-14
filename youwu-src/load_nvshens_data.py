# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "basics.settings")
import django
import re
import time
django.setup()
import json
import random

from load_nvshens_helper import insert_star, parse_star, insert_album, insert_tags

path = os.path.dirname(os.path.realpath(__file__))
items_json = os.path.join(path,
    "../spider/spider_nvshens/myproject/items.json")

file_read = open(items_json, 'r', encoding="utf-8")

info_key = 'info'
image_url_key = 'image_url'


pattern_star_cover = re.compile("https://img\.onvshen\.com:85/girl/\d+\/\d+(_s)?\.jpg")
pattern_album_cover = re.compile("https://img\.onvshen\.com:85/gallery/\d+/\d+/cover/[0-9]+\.jpg")
pattern_album_image = re.compile("https://img\.onvshen\.com:85/gallery/\d+/\d+(/s/)?/\d+\.jpg")


assert pattern_star_cover.match("https://img.onvshen.com:85/girl/22100/22100.jpg")
assert pattern_star_cover.match("https://img.onvshen.com:85/girl/22100/22100_s.jpg")
assert pattern_album_cover.match("https://img.onvshen.com:85/gallery/22100/18017/cover/0.jpg")
assert pattern_album_cover.match("https://img.onvshen.com:85/gallery/23391/22100/cover/0.jpg")
assert pattern_album_image.match("https://img.onvshen.com:85/gallery/22100/18017/015.jpg")


starCover = {}
starInfo = {}
starAlbum = {}
starAlbumCover = {}
albumToStar = {}

tag_id_to_name = {}
tag_id_to_album = {}

noMatchData = []


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
    if url not in to[id]:
        to[id].append(url)

lineNum = 0
lineNumLimit = 20000000

star_id_start= 22000
star_id_end = 22200

for line in file_read:

    if lineNum <= lineNumLimit:
        lineNum += 1
    else:
        break

    if len(line) <= 10:
        continue
    line = line.strip().strip(",")
    data = json.loads(line)

    if 'type' not in data:
        print("error : do not have type !  ---  ")
        print(data)

    if data['type'] == 'info':
        try:
            info = data[info_key]
            info = parse_star(info)
            if 'starId' not in info:
                continue
            starInfo[info['starId']] = info
        except:
            print("error in parse : " + json.dumps(data[info_key]))

    # elif data['type'] == 'AlbumCover':
    #     image_url = data['url']
    #     if pattern_star_cover.match(image_url):
    #         try:
    #             star_id = re.search(r'(\d+)', image_url[re.search('girl', image_url).span()[1]:]).group()
    #             if star_id is not None:
    #                 append_star_cover(star_id, image_url)
    #         except:
    #             print("pattern_star_cover fail : " + image_url)
    elif data['type'] == 'AlbumCover':
        url = data['url']
        star_id = data['star_id']
        album_id = data['album_id']
        albumToStar[album_id] = star_id
        append_album_cover(album_id, url)
    elif data['type'] == 'AlbumImage':
        url = data['url']
        star_id = data['star_id']
        album_id = data['album_id']
        albumToStar[album_id] = star_id
        append_album(album_id, url)
    elif data['type'] == 'TagPage':
        tag_id = data['tagId']
        tag_name = data['tagName']
        album_id_list = data['albumIDList']

        tag_id_to_name[tag_id] = tag_name
        if tag_id in tag_id_to_album:
            tag_id_to_album[tag_id] = tag_id_to_album[tag_id] + album_id_list
        else:
            tag_id_to_album[tag_id] = album_id_list
    else:
        noMatchData.append(data)

for star_id in starInfo.keys():
    if int(star_id) > star_id_end or int(star_id) < star_id_start:
        continue
    star_info = starInfo[star_id]
    star_info['cover'] = ''
    star_id_str = str(star_id)
    if star_id_str in starCover:
        star_info['cover'] = json.dumps(starCover[star_id_str])
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


for k in tag_id_to_name:
    tag = {}
    tagId = k
    tagName = tag_id_to_name[tagId]
    albumIDList = json.dumps(tag_id_to_album[tagId])

    tag['tagId'] = tagId
    tag['tagName'] = tagName
    tag['albumIdList'] = albumIDList

    insert_tags(tag)

with open('noMatchUrl.json', 'w') as outfile:
    json.dump(noMatchData, outfile)

with open('starAlbumCover.json', 'w') as outfile:
    json.dump(starAlbumCover, outfile)

with open('starAlbum.json', 'w') as outfile:
    json.dump(starAlbum, outfile)

with open('starCover.json', 'w') as outfile:
    json.dump(starCover, outfile)


