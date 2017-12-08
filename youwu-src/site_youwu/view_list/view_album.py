from django.shortcuts import render
from django.shortcuts import HttpResponse
from site_youwu.models import album
from site_youwu.models import star
from .view_common  import paging
import random


"""
class album(models.Model):
    name = models.CharField(max_length = 100)
    starName = models.CharField(max_length = 50)
    starID = models.IntegerField()
    picUrl = models.TextField()
    tag = models.CharField(max_length = 50)
    pictureCnt = models.IntegerField()
    publishDate = models.CharField(max_length=15)
    cover = models.URLField()
    des = models.TextField()
    company = models.CharField(max_length = 30)
    termID = models.PositiveIntegerField()   #第几期
    lastModified = models.DateField()

class star(models.Model):
    name = models.CharField(max_length = 50)  #个人名字
    birthday = models.CharField(max_length = 20) #生日
    threeD = models.CharField(max_length = 15)  #三维
    hobby = models.CharField(max_length = 40)  #兴趣爱好
    wordPlace = models.CharField(max_length = 15)  #所在地
    albumID = models.CharField(max_length =300)  #专辑id 逗号隔开
    des = models.TextField()   #个人描述
    tag = models.CharField(max_length = 50)   #个人标签
    cover = models.URLField()  #个人封面
    lastModified = models.DateField(default=timezone.now)
"""

def recommend():
    # 生成一个随机数数组
    count_all = album.objects.count()
    recom_list = list()
    recom_list_length = 0
    re_count = 6

    while recom_list_length <= re_count:

        rand = random.randint(1,count_all)
        if rand not in recom_list:
            recom_list.append(rand)
        recom_list_length = len(recom_list)
    return recom_list


def album_page(request,albumID,pageID):       # pageID: 专辑下的第几页
    data = album.objects.filter(id = albumID)
    name = data.values('name')[0]['name']
    tag = data.values('tag')[0]['tag'].replace("'","").replace("[","").replace("]","").replace(" ","").split(',')   #原数据待修改
    des = data.values('des')[0]['des']
    print(tag)

    picUrlAll = data.values('picUrl')[0]['picUrl'].strip(",").split(',')
    print("len of picUrlAll:", len(picUrlAll))

    content_page = paging(picUrlAll, pageID, 5, 10)   # 5个图片一个页面  每个页面展现10个分页tag
    showData = content_page['showData']

    pageGroup = content_page['pageGroup']

    star_name = data.values('starName')[0]['starName']
    starID = data.values("starID")[0]["starID"]

    star_cover = star.objects.filter(id = starID ).values("cover")[0]["cover"]

    star_des = star.objects.filter(id = starID ).values("des")[0]["des"]

    pageID = int(pageID)
    albumID = int(albumID)



    print(star_cover,star_des)

    print(recommend())

    print("showData:",showData)

    print("albumID:",albumID)
    print("pageID:", pageID)
    print("pageGroup",pageGroup)


    return render(request,"album.html",locals())
