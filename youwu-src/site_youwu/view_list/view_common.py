from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math


def paging(data, current_page, content_cnt, page_num):   # 对内容分页，并且对分页进行分组
    # data:需要进行翻页的数据,通常是所有数据
    # current_page:当前展现的是第几页
    # content_cnt:一页有多少内容;
    # page_num:分页每组展现多少个标签；


    current_page=int(current_page)

    paginator = Paginator(data,content_cnt)
    try:
        showData = paginator.page(current_page) # 获取当前页码的记录
    except PageNotAnInteger:
        showData = paginator.page(1) # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        showData = paginator.page(paginator.num_pages) # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容


    if current_page > paginator.count:
        current_page = paginator.count

    groupCount = page_num
    group = math.ceil(current_page/groupCount)  #当 前分页在第几组

    pageGroup = Paginator(range(1,paginator.num_pages+1),groupCount).page(group).object_list

    return {"showData":showData,"pageGroup":pageGroup}

