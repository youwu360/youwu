# -*- coding: utf-8 -*-


import os
import json
import random
import datetime
from django.db.models import Max

from site_youwu.models import Star, Album, Tags


def insert_star(info):
    print("in insert_star !!!!! ")

    if info is None or type(info) is not dict or 'starId' not in info:
        print("insert star fail : " + json.dumps(info))
        return False

    try:
        if Star.objects.filter(starId=info['starId']).exists():
            Star.objects.get(starId=info['starId']).delete()
    except Exception as e:
        print("try delete fail in insert_star")
        print(e)

    try:
        Star.objects.create(
            starId=info['starId'],
            name=info['name'],
            cover=info['cover'],
            birthday=info['birthday'],
            threeD=info['threeD'],
            height=info['height'],
            weight=info['weight'],
            hobby=info['hobby'],
            birthPlace=info['birthPlace'],
            description=info['description'],
            work=info['work'],
            tag=info['tag']
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
        if Album.objects.filter(albumId=info['albumId']).exists():
            Album.objects.get(albumId=info['albumId']).delete()
    except:
        print("try delete fail in insert_album")

    try:
        Album.objects.create(
            starId=int(info['starId']),
            albumId=int(info['albumId']),
            cover=info['cover'],
            imageListFile=info['imageListFile'],
            pictureCnt=info['pictureCnt'],
            company=info['company'],
            description=info['Description'],
            name=info['Name'],
            publishDate=info['publishDate'],
            tag=info['tag'],
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
        if Tags.objects.filter(tagId=tag['tagId']).exists():
            Tags.objects.get(tagId=tag['tagId']).delete()
    except:
        print("try delete fail in insert_tags")
        print(tag)
    try:
        Tags.objects.create(
            tagId=tag['tagId'],
            tagName=tag['tagName'],
            IdList=tag['IdList'],
            tagTypeId=tag['tagTypeId'],
        )
        print("insert_tags success ！")
        return True
    except Exception as e:
        print("insert error :" + str(tag))
        print(e)
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
