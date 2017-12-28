from django.shortcuts import render
from django.shortcuts import HttpResponse
from site_youwu.models import Album
from site_youwu.models import Star
from .view_common import paging
from .view_common import getAlbumPageUrl
from .view_common import recommend
from .view_common import get_image_list
from .view_common import recom_albums
import json

def album_page(request,albumId,pageId):       # pageID: 专辑下的第几页
    #整数化
    pageId = int(pageId)
    albumId = int(albumId)

    data = Album.objects.filter(albumId = albumId)
    name = data.values('name')[0]['name']
    tag = data.values('tag')[0]['tag'].replace("'","").replace("[","").replace("]","").replace(" ","").split(',')   #原数据待修改
    des = data.values('description')[0]['description']
    starId = data.values("starId")[0]["starId"]

    image_list = get_image_list(starId,albumId)


    page_content = paging(image_list, pageId, 5, 10)   # 5个图片一个页面  每个页面展现10个分页tag
    showData = page_content['showData']
    pageGroup = page_content['pageGroup']
    currentPage = pageId
    url_cut = "/albumId=" + str(albumId) + "/pageId="



    # 明星信息
    star_name = Star.objects.filter(starId=starId).values("name")[0]["name"]
    star_cover = json.loads(Star.objects.filter(starId = starId).values("cover")[0]["cover"])[0]
    star_des = Star.objects.filter(starId = starId).values("description")[0]["description"]
    star_birthday = Star.objects.filter(starId=starId).values("birthday")[0]["birthday"]
    star_threeD =  Star.objects.filter(starId=starId).values("threeD")[0]["threeD"]
    star_hobby = Star.objects.filter(starId=starId).values("hobby")[0]["hobby"]
    star_birthPlace = Star.objects.filter(starId=starId).values("birthPlace")[0]["birthPlace"]

    # 推荐图册
    recom_data = recom_albums(10)


    return render(request,"album.html",locals())
