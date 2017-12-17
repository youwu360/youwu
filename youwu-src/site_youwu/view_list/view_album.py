from django.shortcuts import render
from django.shortcuts import HttpResponse
from site_youwu.models import Album
from site_youwu.models import Star
from .view_common import paging
from .view_common import getAlbumPageUrl
from .view_common import recommend

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


def album_page(request,albumID,pageID):       # pageID: 专辑下的第几页
    #整数化
    pageID = int(pageID)
    albumID = int(albumID)

    data = Album.objects.filter(id=albumID)
    name = data.values('name')[0]['name']
    tag = data.values('tag')[0]['tag'].replace("'","").replace("[","").replace("]","").replace(" ","").split(',')   #原数据待修改
    des = data.values('des')[0]['des']

    picUrlAll = data.values('picUrl')[0]['picUrl'].strip(",").split(',')
    print("len of picUrlAll:", len(picUrlAll))

    content_page = paging(picUrlAll, pageID, 5, 10)   # 5个图片一个页面  每个页面展现10个分页tag
    showData = content_page['showData']

    pageGroup = content_page['pageGroup']

    star_name = data.values('starName')[0]['starName']
    starID = data.values("starID")[0]["starID"]


    # 明星信息
    star_cover = Star.objects.filter(id = starID).values("cover")[0]["cover"]
    star_des = Star.objects.filter(id = starID).values("des")[0]["des"]
    star_birthday = Star.objects.filter(id=starID).values("birthday")[0]["birthday"]
    star_threeD =  Star.objects.filter(id=starID).values("threeD")[0]["threeD"]
    star_hobby = Star.objects.filter(id=starID).values("hobby")[0]["hobby"]
    star_wordPlace = Star.objects.filter(id=starID).values("wordPlace")[0]["wordPlace"]





    # 图片推荐

    albumID_list = recommend(8)

    temp_data = map(lambda x: Album.objects.filter(id = x).values("id", "name", "cover")[0], albumID_list)
    recom_data = list()
    for a in temp_data:   # 增加url
        a["url"] = getAlbumPageUrl(a["id"])
        recom_data.append(a)


    return render(request,"album.html",locals())
