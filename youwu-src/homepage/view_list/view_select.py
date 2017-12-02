from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def select(request):
    return render(request, 'select.html')

