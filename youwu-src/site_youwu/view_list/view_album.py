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


"""
def recommend():
    range = album.objects.count()
    re_list = list()
    re_count = 6
    for i in range( 1,re_count + 1 ):


"""










def album_page(request,albumID,pageID):       #pageID 专辑下的第几页
    data = album.objects.filter(id = albumID)
    name = data.values('name')[0]['name']
    tag = data.values('tag')[0]['tag'].replace("'","").replace("[","").replace("]","").replace(" ","").split(',')   #原数据待修改
    des = data.values('des')[0]['des']
    print(tag)

    picUrlAll = data.values('picUrl')[0]['picUrl'].strip(",").split(',')


    content_page = paging(picUrlAll,pageID,5,10)
    showData = content_page['showData']

    pageGroup = content_page['pageGroup']
    star_name = data.values('starName')[0]['starName']
    starID = data.values("starID")[0]["starID"]

    star_cover = star.objects.filter(id = starID ).values("cover")[0]["cover"]

    star_des = star.objects.filter(id = starID ).values("des")[0]["des"]

    print(star_cover,star_des)










    return render(request,"album.html",locals())
