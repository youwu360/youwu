from django.shortcuts import render
from django.shortcuts import HttpResponse
from site_youwu.models import Album
from site_youwu.models import Star
from site_youwu.models import Tags
from .view_common import paging
from .view_common import getAlbumPageUrl
from .view_common import recommend
from .view_common import recom_albums
import json

def classify_page_default(request,tagId,pageId):




    return render(request, "classify.html", locals())




def classify_page(request,tagId,pageId):

    tagId = int(tagId)
    pageId = int(pageId)

    # tag 列表
    type = Tags.objects.all().values("tagTypeId","tagTypeName").distinct()
    tag_data = []
    for line in type:
        line["tag_list"] = list(Tags.objects.filter(tagTypeId=line["tagTypeId"]).values("tagId","tagName").distinct())
        tag_data.append(line)

    # 当前tag对应的albums
    albumId = Tags.objects.filter(tagId = tagId).values("albumId")[0]["albumId"].split(',')
    albums = list(map(lambda x : Album.objects.filter( albumId = x).values("name","cover","albumId")[0],albumId))
    for line in albums:
        #print(line)
        line["cover"] = json.loads(line["cover"])[0]
        line["to_url"] = getAlbumPageUrl(line["albumId"])


    # 分页
    page_content = paging(albums, pageId, 40, 10)   # 40个图片一个页面  每个页面展现10个分页tag
    showData = page_content['showData']
    pageGroup = page_content['pageGroup']
    currentPage = pageId

    url_cut = "/tagId=" + str(tagId) + "/pageId="

    # 推荐的albums
    recom_album = recom_albums(10)

    return render(request, "classify.html", locals())
