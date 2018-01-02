from django.shortcuts import render
from site_youwu.models import Album
from .view_common import getAlbumPageUrl
from .view_common import is_mobile_check
from .view_common import paging

# Create your views here.

def home_page(request,pageId):
    agent = request.META.get('HTTP_USER_AGENT')
    is_mobile = is_mobile_check(agent)
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

