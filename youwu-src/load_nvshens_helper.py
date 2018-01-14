# -*- coding: utf-8 -*-


import os
import json
import random
import datetime
from django.db.models import Max

from site_youwu.models import Star, Album, Tags


def get_value_by_tag(line, tag):
    for i in range(0, len(line), 2):
        if tag == line[i]:
            return line[i + 1]
    return None


def parse_star(line):
    if type(line) is not list or len(line) < 5:
        return None
    info = {}
    info['starId'] = get_value_by_tag(line, 'starId')
    info['name'] = get_value_by_tag(line, 'name')
    info['cover'] = get_value_by_tag(line, 'cover')
    info['birthday'] = get_value_by_tag(line, '生 日：')
    info['threeD'] = get_value_by_tag(line, '三 围：')
    info['height'] = get_value_by_tag(line, '身 高：')
    weight_str= get_value_by_tag(line, '体 重：')
    if weight_str is not None:
        weight_data = weight_str.split(" ")
        info['weight'] = float(weight_data[0])
    else:
        info['weight'] = -1

    info['hobby'] = get_value_by_tag(line, '兴 趣：')
    info['birthPlace'] = get_value_by_tag(line, '出 生：')
    info['description'] = get_value_by_tag(line, 'description')
    info['tag'] = get_value_by_tag(line, 'tag')

    return info


def insert_star(info):
    print("in insert_star !!!!! ")

    if info is None or type(info) is not dict or 'starId' not in info:
        print("insert star fail : " + json.dumps(info))
        return False

    try:
        exists = Star.objects.get(starId=info['starId'])
        if exists is not None:
            print("start delete star : starId:" + str(info['starId']))
            exists.delete()
            print("end delete star : starId:" + str(info['starId']))
    except Exception as e:
        print("try delete fail in insert_star")
        print(e)

    try:
        Star.objects.create(
            starId = info['starId'],
            name = info['name'],
            cover = info['cover'],
            birthday = info['birthday'],
            threeD = info['threeD'],
            height = info['height'],
            weight = info['weight'],
            hobby = info['hobby'],
            birthPlace = info['birthPlace'],
            description = info['description'],
            tag = info['tag']
        )
        print("insert_star success ！")
        return True
    except:
        print("insert error :" + str(info))

    return False


def insert_album(info):
    print('in insert_album !!!! ')
    if info is None or type(info) is not dict or 'albumId' not in info:
        print("insert album fail " + json.dumps(info))
        return False

    try:
        exists = Album.objects.get(albumId=info['albumId'])
        if exists is not None:
            print("start delete album : starId:" + str(info['albumId']))
            exists.delete()
            print("end delete album : starId:" + str(info['albumId']))
    except:
        print("try delete fail in insert_album")

    try:
        Album.objects.create(
            starId = info['starId'],
            albumId = info['albumId'],
            cover = info['cover'],
            imageListFile = info['imageListFile'],
            pictureCnt = info['pictureCnt'],
        )
        print("insert_album success ！")
        return True
    except:
        print("insert error :" + str(info))
    return False


def insert_tags(tag):
    if tag is None or type(tag) is not dict or 'tagId' not in tag:
        print("insert tag fail " + json.dumps(tag))
        return False

    try:
        exists = Tags.objects.get(tagId=tag['tagId'])
        if exists is not None:
            print("start delete tag : tagId:" + str(tag['tagId']))
            exists.delete()
            print("end delete tag : tagId:" + str(tag['tagId']))
    except:
        print("try delete fail in insert_tags")

    try:
        Tags.objects.create(
            tagId = tag['tagId'],
            tagName = tag['tagName'],
            albumIdList = tag['albumIdList'],
        )
        print("insert_tags success ！")
        return True
    except:
        print("insert error :" + str(tag))
    return False

def update_tag_type_and_name(tagName, tagTypeId, tagTypeName):
    if tagName is None or tagTypeName is None:
        print('insert value error. tagName:' + str(tagName) +
              " tagTypeName" + str(tagTypeName))
    try:
        Tags.objects.filter(tagName=tagName).\
            update(tagTypeName=tagTypeName)

        Tags.objects.filter(tagName=tagName). \
            update(tagTypeId=tagTypeId)
    except:
        print('update tag error')
