from django.shortcuts import render
from django.shortcuts import HttpResponse
from site_youwu.models import album
from site_youwu.models import star
from .view_common import paging
from .view_common import getAlbumPageUrl
from .view_common import recommend

def classify(request,tagID,pageID):



    return render(request, "classify.html", locals())
