from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .. import models

page_star_count = 12


def select(request, page_num):
    star_list = models.star.objects.all()
    paginator = Paginator(star_list, page_star_count)

    current_page_num = int(page_num)
    try:
        data_star_page = paginator.page(current_page_num)
    except PageNotAnInteger:
        data_star_page = paginator.page(1)
    except EmptyPage:
        data_star_page = paginator.page(paginator.num_pages)

    page_range = range(1, 1 + paginator.num_pages)
    return render(request, 'select.html',
                  {'data_star_page': data_star_page,
                   'current_page_num': current_page_num,
                   'page_range': page_range,
                   })

