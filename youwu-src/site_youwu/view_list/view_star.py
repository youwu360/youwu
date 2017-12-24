from django.shortcuts import render
from django.shortcuts import HttpResponse
from site_youwu.models import Album
from site_youwu.models import Star
from .view_common import paging
from .view_common import getAlbumPageUrl
from .view_common import recommend
from .view_common import recom_albums
import json

def star_page(request,starId,pageId):

    # 基础信息
    starId = int(starId)
    pageId = int(pageId)
    star_info = Star.objects.filter(starId=starId)
    star_name = star_info.values("name")[0]["name"]
    star_threeD = star_info.values("threeD")[0]["threeD"]
    star_hobby = star_info.values("hobby")[0]["hobby"]
    star_birthday = star_info.values("birthday")[0]["birthday"]
    star_birthPlace = star_info.values("birthPlace")[0]["birthPlace"]
    star_cover = star_info.values("cover")[0]["cover"]
    star_height = star_info.values("height")[0]["height"]
    star_weight = star_info.values("weight")[0]["weight"]
    star_description = star_info.values("description")[0]["description"]

    # star 对应的图册
    album_temp = Album.objects.filter(starId= starId).values("albumId", "name", "cover")
    star_album = []
    for a in album_temp:   # 增加url
        a["cover"] = json.loads(a["cover"])[0]
        a["to_url"] = getAlbumPageUrl(a["albumId"])
        star_album.append(a)


    # 分页
    page_content = paging(star_album, pageId, 40, 10)   # 40个图片一个页面  每个页面展现10个分页tag
    showData = page_content['showData']
    pageGroup = page_content['pageGroup']
    currentPage = pageId

    url_cut = "/starId=" + str(starId) + "/pageId="

    # 推荐图册
    recom_data = recom_albums(10)




    return render(request, "star.html", locals())
