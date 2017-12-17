from django.shortcuts import render
from django.shortcuts import HttpResponse
from site_youwu.models import Album
from site_youwu.models import Star
from .view_common import paging
from .view_common import getAlbumPageUrl
from .view_common import recommend

def star_page(request,starID):

    # 基础信息
    starID = int(starID)
    star_info = Star.objects.filter(id=starID)
    name = star_info.values("name")[0]["name"]
    threeD = star_info.values("threeD")[0]["threeD"]
    hobby = star_info.values("hobby")[0]["hobby"]
    birthday = star_info.values("birthday")[0]["birthday"]
    workPlace = star_info.values("workPlace")[0]["workPlace"]
    cover = star_info.values("cover")[0]["cover"]

    # star 对应的图册
    albumID_list = star_info.values("albumID")[0]["albumID"].split(',')   # 一个list
    temp_data = map(lambda x: Album.objects.filter(id = x).values("id", "name", "cover")[0], albumID_list)
    star_ablum = list()
    for a in temp_data:   # 增加url
        a["url"] = getAlbumPageUrl(a["id"])
        star_ablum.append(a)

    print(star_ablum)

    return render(request, "star.html", locals())
