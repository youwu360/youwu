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
import logging
logger = logging.getLogger(__name__)


def album_page(request,albumId,pageId):       # pageID: 专辑下的第几页

    pageId = int(pageId)
    albumId = int(albumId)

    # 检查请求是否来自移动端
    is_mobile = is_mobile_check(request)

    data = Album.objects.filter(albumId=albumId)
    name = data.values('name')[0]['name']
    tag = data.values('tag')[0]['tag'].replace("'","").replace("[","").replace("]","").replace(" ","").split(',')   #原数据待修改
    des = data.values('description')[0]['description']
    starId = data.values("starId")[0]["starId"]
    image_list = get_image_list(starId, albumId)

    # 参数配置
    if is_mobile:
        page_cnt = 5
        re_com_cnt = 6
    else:
        page_cnt = 10
        re_com_cnt = 10

    # 分页
    try:
        page_content = paging(image_list, pageId, 5, page_cnt)   # 5个图片一个页面  每个页面展现10个分页tag
        showData = page_content['showData']
        pageGroup = page_content['pageGroup']
        currentPage = pageId
        url_cut = "/albumId=" + str(albumId) + "/pageId="
    except Exception as e:
        print(e)

    # 明星信息
    logger.error('=====================================')
    logger.error(starId)

    star_name =""
    query_set = Star.objects.filter(starId=starId)
    if query_set is not None and query_set.exists():
        star_name = query_set.values("name")[0]["name"]
        star_cover = json.loads(query_set.values("cover")[0]["cover"])[0]
        star_des = query_set.values("description")[0]["description"]
        star_birthday = query_set.values("birthday")[0]["birthday"]
        star_threeD = query_set.values("threeD")[0]["threeD"]
        star_hobby = query_set.values("hobby")[0]["hobby"]
        star_birthPlace = query_set.values("birthPlace")[0]["birthPlace"]

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
