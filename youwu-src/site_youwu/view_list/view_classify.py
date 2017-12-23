from django.shortcuts import render
from django.shortcuts import HttpResponse
from site_youwu.models import Album
from site_youwu.models import Star
from .view_common import paging
from .view_common import getAlbumPageUrl
from .view_common import recommend

def classify_page_default(request,tagId,pageId):




    return render(request, "classify.html", locals())




def classify_page(request,tagId,pageId):

    tagId = int(tagId)
    pageId = int(pageId)





    return render(request, "classify.html", locals())
