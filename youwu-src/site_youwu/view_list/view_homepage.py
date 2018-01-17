from django.shortcuts import render
from site_youwu.models import Album
from .view_common import getAlbumPageUrl
from .view_common import is_mobile_check
from .view_common import paging

# Create your views here.

def home_page(request,*ids):

    # seo_info
    title = "尤物丝_美女图片社区"
    keywords = "宅男女神、美女图片、推女郎、推女神、尤果"
    description = "每日更新最新美女图片、女神资料，最受欢迎的美女图片社区。"

    if len(ids) == 0:
        pageId = 1
    else:
        pageId= ids[0]

    is_mobile = is_mobile_check(request)

    data = Album.objects.all().values("name", "cover", "albumId")

    res =[]
    for line in data:
        line["cover"] = line["cover"].strip("[").strip("]").strip('"')
        line["album_url"] = getAlbumPageUrl(line["albumId"])
        #print(line)

    # 分页
    if is_mobile:
        album_cnt = 15     # 每页展现多少内容
        paging_cnt = 5        # 展现多少个分页
    else:
        album_cnt = 30    # 每页展现多少内容
        paging_cnt = 10        # 展现多少个分页

    page_content = paging(data, pageId, album_cnt, paging_cnt)
    showData = page_content['showData']
    pageGroup = page_content['pageGroup']
    currentPage = int(pageId) #从url中获取当前页数
    url_cut = "/index="

    # 根据移动端和pc端返回不同的结果
    if is_mobile:
        return render(request, "m_home.html", locals())
    else:
        return render(request, "home.html", locals())



