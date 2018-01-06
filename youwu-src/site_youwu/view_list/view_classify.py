from django.shortcuts import render
from django.shortcuts import HttpResponse
from site_youwu.models import Album
from site_youwu.models import Star
from site_youwu.models import Tags
from .view_common import paging
from .view_common import getAlbumPageUrl
from .view_common import recommend
from .view_common import recom_albums
from .view_common import getAlbumInfoById
import json
from .view_common import is_mobile_check


def classify_page(request,*ids):

    is_mobile = is_mobile_check(request)

    # tag 列表
    type = Tags.objects.all().values("tagTypeId","tagTypeName").distinct()
    tag_data = []
    for line in type:
        line["tag_list"] = list(Tags.objects.filter(tagTypeId=line["tagTypeId"]).values("tagId","tagName").distinct())
        tag_data.append(line)

    # 当前tag对应的albums   如果没有带参数，则返回列表
    if len(ids) > 1 :
        tagId = int(ids[0])
        pageId = int(ids[1])
        albumId = Tags.objects.filter(tagId = tagId).values("albumId")[0]["albumId"].split(',')
        albums = list(map(lambda x : Album.objects.filter( albumId = x).values("name","cover","albumId")[0],albumId))
        for line in albums:
            #print(line)
            line["cover"] = json.loads(line["cover"])[0]
            line["to_url"] = getAlbumPageUrl(line["albumId"])
        url_cut = "/tagId=" + str(tagId) + "/pageId="

    else:
        pageId = int(ids[0])
        albumId_list = Album.objects.all().values("albumId")
        albums = getAlbumInfoById(albumId_list)
        url_cut =  "/tag/pageId="


    # 分页
    page_content = paging(albums, pageId, 40, 10)   # 40个图片一个页面  每个页面展现10个分页tag
    showData = page_content['showData']
    pageGroup = page_content['pageGroup']
    currentPage = pageId



    # 推荐的albums
    #recom_album = recom_albums(10)


    return render(request, "classify.html", locals())
