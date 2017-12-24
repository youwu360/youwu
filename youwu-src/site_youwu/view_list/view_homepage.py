from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math
from site_youwu.models import Album
from site_youwu.models import Star
from .view_common import addAttrToList
from .view_common import getAlbumPageUrl



# Create your views here.



def home_page(request,page):


    data = Album.objects.all().values("name", "cover", "albumId")

    res =[]
    for line in data:
        line["cover"] = line["cover"].strip("[").strip("]").strip('"')
        line["album_url"] = getAlbumPageUrl(line["albumId"])
        print(line)
        

    paginator = Paginator(data,30)
    currentPage = int(page) #从url中获取当前页数

    try:
        showData = paginator.page(currentPage)#获取当前页码的记录
    except PageNotAnInteger:
        showData = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        showData = paginator.page(paginator.num_pages)#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容



    if currentPage > paginator.count:
        currentPage = paginator.count

    groupCount = 10
    group = math.ceil(currentPage/groupCount)  #当前分页在第几组

    pageGroup = Paginator(range(1,paginator.num_pages+1),groupCount).page(group).object_list
    #print(pageGroup)


    return render(request,"home.html",locals())

