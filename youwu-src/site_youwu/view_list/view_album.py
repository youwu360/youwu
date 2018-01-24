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
from .view_common import is_mobile_check
from .view_common import get_hot_tags


def album_page(request,albumId,pageId):       # pageID: 专辑下的第几页



    #整数化
    pageId = int(pageId)
    albumId = int(albumId)

    # 检查请求是否来自移动端
    is_mobile = is_mobile_check(request)

    data = Album.objects.filter(albumId = albumId)
    name = data.values('name')[0]['name']
    tag = data.values('tag')[0]['tag'].replace("'","").replace("[","").replace("]","").replace(" ","").split(',')   #原数据待修改
    des = data.values('description')[0]['description']
    starId = data.values("starId")[0]["starId"]
    image_list = get_image_list(starId,albumId)

    # 参数配置
    if is_mobile:
        page_cnt = 5
        re_com_cnt = 6
    else:
        page_cnt = 10
        re_com_cnt = 10

    # 分页
    page_content = paging(image_list, pageId, 5, page_cnt)   # 5个图片一个页面  每个页面展现10个分页tag
    showData = page_content['showData']
    pageGroup = page_content['pageGroup']
    currentPage = pageId
    url_cut = "/albumId=" + str(albumId) + "/pageId="

    # 明星信息
    star_name = Star.objects.filter(starId=starId).values("name")[0]["name"]
    star_cover = json.loads(Star.objects.filter(starId = starId).values("cover")[0]["cover"])[0]
    star_des = Star.objects.filter(starId = starId).values("description")[0]["description"]
    star_birthday = Star.objects.filter(starId=starId).values("birthday")[0]["birthday"]
    star_threeD = Star.objects.filter(starId=starId).values("threeD")[0]["threeD"]
    star_hobby = Star.objects.filter(starId=starId).values("hobby")[0]["hobby"]
    star_birthPlace = Star.objects.filter(starId=starId).values("birthPlace")[0]["birthPlace"]

    # seo_info
    title = str(star_name) + "_" + str(name) + "_尤物丝"
    keywords = str(star_name)
    for line in tag:
        keywords = keywords + "," + line
    description = des + star_name

    # 推荐图册
    recom_data = recom_albums(re_com_cnt)

    # 热门分类
    hot_tags = get_hot_tags()

    if is_mobile:
        return render(request, "m_album.html", locals())
    else:
        return render(request, "album.html", locals())
