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
from .view_common import get_hot_tags
from .show_tags import get_tags
import json
import sys
import os



def classify_page(request, *ids):

    page_type = 'classify'  # 页面类型

    is_mobile = is_mobile_check(request)

    # 参数配置
    if is_mobile:
        page_cnt = 5
        content_cnt = 15
    else:
        page_cnt = 10
        content_cnt = 40


    # tag 列表
    tag_data = get_tags()
    #print(tag_data)


    # 当前tag对应的albums   如果没有带参数，则返回列表
    tagName = ""

    if len(ids) > 1 :    # 标签分类页
        tagId = ids[0]
        pageId = int(ids[1])
        tagName = Tags.objects.filter(tagId = tagId).values("tagName")[0]["tagName"]
        albumId = json.loads(Tags.objects.filter(tagId = tagId).values("IdList")[0]["IdList"])

        albums = []
        for line in albumId:
            item = dict()
            try:
                temp_info = Album.objects.filter( albumId = line).values("name","cover","albumId")[0]
                item["cover"] = json.loads(temp_info["cover"])[0]
                item["name"] = temp_info["name"]
                item["albumId"] = temp_info["albumId"]

            except Exception as e:
                #print(e)
                continue
            albums.append(item)

        m_nav_title = tagName
        url_cut = "/tagId=" + str(tagId) + "/pageId="

    else:       # 总分类页
        pageId = ids[0]
        albumId_temp = Album.objects.all().values("albumId")
        albumId = []
        for line in albumId_temp:
            albumId.append(line["albumId"])
        albums = getAlbumInfoById(albumId)
        url_cut =  "/tag/pageId="

        m_nav_title = "尤物分类"


    # 分页
    page_content = paging(albums, pageId, content_cnt, page_cnt)   # 40个图片一个页面  每个页面展现10个分页tag
    showData = page_content['showData']
    pageGroup = page_content['pageGroup']
    currentPage = pageId

    # 热门分类
    hot_tags = get_hot_tags()

    # 推荐的albums
    #recom_album = recom_albums(10)

    # seo_info
    if len(tagName) >0 :
        title = tagName + "_分类美女专辑_尤物丝"
        keywords = tagName
        description = tagName + "_分类美女专辑_尤物丝"

    else:
        title = "套图分类_尤物丝"
        keywords = "精品套图,套图,美女套图,亚洲套图,欧美套图,套图屋,美女图片"
        description = "免费提供以性感美女, 制服丝袜, 诱惑, 丝袜美腿为一体的高清美女大图片套图在线预览, 打造最受欢迎的美女图片社区。"

        # 返回结果
    if is_mobile and len(ids) == 1:
        return render(request, "m_classify.html", locals())
    elif is_mobile and len(ids) == 2:
        return render(request, "m_classify_detail.html", locals())

    elif is_mobile == False:
        return render(request, "classify.html", locals())
