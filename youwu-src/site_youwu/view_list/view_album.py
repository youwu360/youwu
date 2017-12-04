from django.shortcuts import render
from django.shortcuts import HttpResponse


def album_page(request,albumID):

    return render(request,"view_album.html")
