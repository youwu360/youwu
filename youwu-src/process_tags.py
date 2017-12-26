# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "basics.settings")
import django
import re
import time
django.setup()
import json
import random

from load_nvshens_helper import update_tag_type_and_name


path = os.path.dirname(os.path.realpath(__file__))
tags_json = os.path.join(path, "../spider/spider_nvshens/myproject/tags.json")
tag_data = json.load(open(tags_json, 'r', encoding='utf-8'))

tag_set = set()
for tag in tag_data:
    tag_set.add(tag['tagName'])

tag_info = []
tag_info_name = []
tag_info.append('亚洲 日韩 中国内地 台湾 香港 澳门 日本 韩国 马来西亚 '
                '越南 泰国 菲律宾 混血 欧美 印度 非洲'
                ' 美国 俄罗斯 乌克兰 英国 法国 德国 意大利 西班牙 荷兰 捷克 克罗地亚 '
                '丹麦 土耳其 瑞典 葡萄牙 希腊 爱尔兰 挪威')
tag_info_name.append('area')

tag_info.append('姐妹花 萝莉 妩媚 清新 萌系 治愈系 清纯 气质 性感 冷艳 野性 '
                '诱惑 养眼 大尺度')
tag_info_name.append('character')

tag_info.append('骨感 女神 极品 美腿 波涛胸涌 人间胸器 娇小萝莉 童颜巨乳 '
                '肉感 白嫩 小麦色 蜜桃臀 香肩 玉足 尤物 美臀')
tag_info_name.append('body')

tag_info.append('足球宝贝 篮球宝贝 拳击宝贝 开背毛衣 肚兜 旗袍 空姐 丁字裤'
                ' 和服 比基尼 内衣 制服 角色扮演 校服 护士 湿身 黑丝 女仆')
tag_info_name.append('clothes')

tag_info.append('蜜桃社 尤蜜荟 尤物馆 御女郎 爱蜜社 推女郎 美媛馆 尤果网 嗲囡囡 爱尤物 顽味生活 '
                '秀人网 推女神 魅妍社 波萝社 优星馆 模范学院 星乐园 飞图网 头条女神 青豆客 优果网 '
                '糖果画报 薄荷叶 51modo 果团网 猫萌榜 花漾 克拉女神 影私荟 花の颜 激萌文化 兔几盟')
tag_info_name.append('organization')

tag_info.append('beautyleg RQ-STAR YS-Web套图 DGC套图 Bomb.tv @misty Sabra.net 4K-STAR')
tag_info_name.append('suites')

tag_info.append('沙滩 泳池 户外 街拍 家居 浴室 圣诞 春节 沙漠 私房照')
tag_info_name.append('scenario')

tag_info.append('体育画报:Weekly Big Comic Spirits:Young Champion:Weekly Playboy:Young Magazine:'
                'Weekly Young Jump')
tag_info_name.append('magazine')

generated_tag_set = set()
for line in tag_info:
    sep = ' '
    if ':' in line:
        sep = ':'
    arr = line.split(sep)
    for tag in arr:
        generated_tag_set.add(tag)

assert len(tag_set - generated_tag_set) == 0
assert len(generated_tag_set -tag_set) == 0


for i in range(len(tag_info)):
    sep = ' '
    line = tag_info[i]
    print(line)
    if ':' in line:
        sep = ':'
    arr = line.split(sep)
    print(arr)
    print(tag_info_name[i])
    for tag in arr:
        update_tag_type_and_name(tag, i + 1, tag_info_name[i])
        print('tag : ' + tag + " updated ! ")




