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
import json
import sys
import os



def classify_page(request, *ids):

    is_mobile = is_mobile_check(request)

    # 参数配置
    if is_mobile:
        page_cnt = 5
        content_cnt = 15
    else:
        page_cnt = 10
        content_cnt = 40


    # tag 列表


    type = Tags.objects.all().values("tagTypeId","tagTypeName").distinct()
    tag_data = []
    for line in type:
        line["tag_list"] = list(Tags.objects.filter(tagTypeId=line["tagTypeId"]).values("tagId","tagName").distinct())
        tag_data.append(line)

    """
    tag_data = []
    item = []
    temp_dic = {}
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"show_tags")
    tag_file = open(file_path, "r")

    for line in tag_file:
        if "@" in line:
            temp_dic["tag_list"] = item
            print(temp_dic)
            tag_data.append(temp_dic)
            item = []
            continue
        if len(line.strip()) > 0 :
            line = line.strip()
            item.append(json.loads(line))
        print("+++++++++")

    print("+++++++++")
    print(tag_data)
    """

    # 当前tag对应的albums   如果没有带参数，则返回列表
    tagName = ""

    if len(ids) > 1 :
        tagId = ids[0]
        pageId = int(ids[1])
        tagName = Tags.objects.filter(tagId = tagId).values("tagName")[0]["tagName"]
        albumId = json.loads(Tags.objects.filter(tagId = tagId).values("albumIdList")[0]["albumIdList"])
        #print(albumId)
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
    page_content = paging(albums, pageId, content_cnt, page_cnt)   # 40个图片一个页面  每个页面展现10个分页tag
    showData = page_content['showData']
    pageGroup = page_content['pageGroup']
    currentPage = pageId



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
