from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from homepage.view_list.view_hello import hello
from homepage.view_list.view_select import select

