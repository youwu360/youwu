from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from site_youwu.models import Album
from site_youwu.models import Star
import math
import random
import json
import os
import logging
logger = logging.getLogger(__name__)

allUrlsForProductInJsonFile = '/tmp/allUrlsForProduct.json'
allUrlsForProductInJson = None
if os.path.exists(allUrlsForProductInJsonFile):
    allUrlsForProductInJson = json.load(open(allUrlsForProductInJsonFile))

starCover = 'starCover'
albumCover = 'albumCover'
albumToStar = 'albumToStar'
albumImageList = 'albumImageList'

def get_album_cover(albumId):
    if allUrlsForProductInJson is not None:
        try:
            if str(albumId) in allUrlsForProductInJson[albumCover]:
                return allUrlsForProductInJson[albumCover][(albumId)]
        except:
            pass

def get_star_cover(starId):
    if allUrlsForProductInJson is not None:
        try:
            if str(starId) in allUrlsForProductInJson[starCover]:
                return allUrlsForProductInJson[starCover][str(starId)]
        except:
            pass

def get_image_list(starId, albumId):
    if allUrlsForProductInJson is not None:
        try:
            if str(albumId) in allUrlsForProductInJson[albumImageList]:
                return list(allUrlsForProductInJson[albumImageList][str(albumId)].values())
        except:
            pass
    path = os.path.abspath(os.path.join(os.path.realpath(__file__),
        "../../../../youwu-resource/data/url_info/"
        + str(starId) + "."
        + str(albumId)))
    try:
        file_open = open(path, 'r')
        obj = json.load(file_open)
    except:
        obj = None
    return obj

def paging(data, current_page, content_cnt, page_num):   # 对内容分页，并且对分页进行分组
    # data:需要进行翻页的数据,通常是所有数据；
    # current_page:当前展现的是第几页；
    # content_cnt:一页有多少内容;
    # page_num:分页每组展现多少个标签；
    current_page=int(current_page)
    paginator = Paginator(data,content_cnt)
    try:
        showData = paginator.page(current_page) # 获取当前页码的记录
    except PageNotAnInteger:
        showData = paginator.page(1) # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        showData = paginator.page(paginator.num_pages) # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    if current_page > paginator.count:
        current_page = paginator.count



    # 定义当前页排序
    if page_num <= 5:
        index = 3
    else:
        index = 5
    """
    # 定义最小分页
    if current_page - index > 0:
        min_index = current_page - index
    elif current_page - index <= 0:
        min_index = 1

    # 定义最大分页
    if current_page + page_num - index <= paginator.num_pages:
        max_index = max(page_num, current_page + page_num - index -1)
    else:
        max_index = paginator.num_pages


    # 尾部极端情况
    if paginator.num_pages - current_page < page_num -index :
        max_index = paginator.num_pages
        min_index = paginator.num_pages - page_num + 1

    # 头部极端情况
    if paginator.num_pages < index:
        min_index = 1
        max_index = paginator.num_pages
    """

    a_dis = index - 1
    b_dis = page_num - index

    if page_num >= paginator.num_pages:
        min_index = 1
        max_index = paginator.num_pages
    elif page_num < paginator.num_pages:
        if current_page - a_dis > 0 and current_page + b_dis <= paginator.num_pages:
            min_index = current_page - a_dis
            max_index = current_page + b_dis
        elif current_page - a_dis > 0 and current_page + b_dis > paginator.num_pages:
            min_index = paginator.num_pages - page_num +1
            max_index = paginator.num_pages
        elif current_page - a_dis <= 0:
            min_index = 1
            max_index = page_num

    pageGroup = range(min_index, max_index+1)

    return {"showData":showData,"pageGroup":pageGroup}


def getAlbumPageUrl(ablumId):
    # 通过albumID 获取 专辑页的ulr
    url = "/albumId=" + str(ablumId) + "/" + "pageId=1" + "/"
    return url


def recommend(x):
    # 生成一个随机数数组
    count_all = Album.objects.count()
    #print(count_all)
    recom_list = list()
    recom_list_length = 0
    re_count = x
    albumId = []   # 最后的输出
    while recom_list_length < re_count:
        rand = random.randint(1, count_all)
        if rand not in recom_list:
            try:
                albumId.append(Album.objects.filter(id=rand).values("albumId")[0]["albumId"])
            except:
                continue
            recom_list.append(rand)
            recom_list_length = len(recom_list)
    #print(recom_list)
    return albumId

def recom_albums(x):
    albumId_list = recommend(x)

    temp_data = map(lambda x: Album.objects.filter(albumId = x).values("albumId", "name", "cover")[0], albumId_list)
    recom_data = list()
    if temp_data is not None:
        for a in temp_data:   # 增加url
            try:
                a["cover"] = json.loads(a["cover"])[0]
                a["album_url"] = getAlbumPageUrl(a["albumId"])
                recom_data.append(a)
            except Exception as e:
                print(e)
    #print(recom_data)
    return recom_data



def getAlbumInfoById(albumId):

    albums = []
    print(albumId)
    for line in albumId:
        item = dict()
        try:
            temp_info = Album.objects.filter(albumId=line).values("name", "cover", "albumId")[0]
            print(temp_info)
            item["cover"] = json.loads(temp_info["cover"])[0]
            item["name"] = temp_info["name"]
            item["albumId"] = temp_info["albumId"]

        except Exception as e:
            print(e)
            continue
        albums.append(item)
    return albums

def addAttrToList(list,func,name,id): # 对词典形成的list，通过函数进行增加内容
    # list：内容列表
    # func:函数
    # name：增加的内容名称
    # id：根据id 字段算出结果
    for dic in list:
        dic[name] = func(dic[id])

def clean_str(string):
    need_to_clean = [" ", "[", "]", "'"]
    for a in need_to_clean:
        string = string.replace(a, "")
    return string


def is_mobile_check(request):
    agent = request.META.get('HTTP_USER_AGENT')
    res = False
    mobile_key = ["iPhone", "iPad", "iPod", "Android"]
    for line in mobile_key:
        if line in agent:
            res = True
            break
    return res


def get_hot_tags():
    hot_tags = [
        {"tagName": "尤物", "tagId": "youwu"},
        {"tagName": "女神", "tagId": "nvshen"},
        {"tagName": "极品", "tagId": "jipin"},
        {"tagName": "肉感", "tagId": "rougan"},
        {"tagName": "人间胸器", "tagId": "xiongqi"},
        {"tagName": "波涛胸涌", "tagId": "botao"},
        {"tagName": "童颜巨乳", "tagId": "tongyanjuru"},
        {"tagName": "大尺度", "tagId": "dachidu"},
        {"tagName": "美臀", "tagId": "meitun"},
        {"tagName": "白嫩", "tagId": "bainen"},
        {"tagName": "气质", "tagId": "qizhi"},
        {"tagName": "美腿", "tagId": "meitui"}
    ]
    return hot_tags


def get_hot_models(x):
    temp_data = Star.objects.all().values("starId", "cover", "name").order_by('?')[:x]
    for line in temp_data:
        line["cover"] = json.loads(line["cover"])[0]
        line["name"] = line["name"].split("(")[0]

    return list(temp_data)


