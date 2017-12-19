from django.shortcuts import render
from django.shortcuts import HttpResponse
from site_youwu.models import Album
from site_youwu.models import Star
from .view_common import paging
from .view_common import getAlbumPageUrl
from .view_common import recommend

def star_page(request,starId):

    # 基础信息
    starId = int(starId)
    star_info = Star.objects.filter(id=starId)
    star_name = star_info.values("name")[0]["name"]
    star_threeD = star_info.values("threeD")[0]["threeD"]
    star_hobby = star_info.values("hobby")[0]["hobby"]
    star_birthday = star_info.values("birthday")[0]["birthday"]
    star_birthPlace = star_info.values("birthPlace")[0]["birthPlace"]
    star_cover = star_info.values("cover")[0]["cover"]
    star_height = star_info.values("height")[0]["height"]
    star_weight = star_info.values("weight")[0]["weight"]

    # star 对应的图册
    album = Album.objects.filter(starID= starId).values("albumId", "name", "cover")
    for a in album:   # 增加url
        a["to_url"] = getAlbumPageUrl(a["albumId"])

    # 推荐图册
    albumId_list = recommend(8)
    temp_data = map(lambda x: Album.objects.filter(albumId = x).values("albumId", "name", "cover")[0], albumId_list)
    recom_data = list()
    for a in temp_data:   # 增加url
        a["album_url"] = getAlbumPageUrl(a["albumId"])
        recom_data.append(a)


    return render(request, "star.html", locals())
