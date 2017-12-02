from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math

# Create your views here.

data = [
    {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
    {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
        {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
        {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
        {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
        {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
        {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
        {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
        {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
        {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
        {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
    {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
    {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
            {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
            {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
            {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
            {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
            {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
            {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
            {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
            {
        "title":"UGirls 尤果写真 No.320  Modo 陈夕",
        "issue_url":"http://www.lsmpic.com/thread-17264-1-1.html",
        "cover_img":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg"
     },
]
def hello(request,page):

    paginator = Paginator(data,6)
    currentPage = int(page) #从url中获取当前页数

    try:
        print(page)
        showData = paginator.page(currentPage)#获取当前页码的记录
    except PageNotAnInteger:
        showData = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        showData = paginator.page(paginator.num_pages)#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    print(showData.has_previous())
    print(showData.has_next())

    if currentPage > paginator.count:
        currentPage = paginator.count
    print("currentPage",currentPage)
    print("paginator.count",paginator.count)

    groupCount = 10
    group = math.ceil(currentPage/groupCount)  #当前分页在第几组

    pageGroup = Paginator(range(1,paginator.num_pages+1),groupCount).page(group).object_list
    print(pageGroup)

    return render(request,"home.html",{"showData":showData,"pageGroup":pageGroup,"currentPage":currentPage})

