from django.db import models
from datetime import datetime
from django.utils import timezone


class Album(models.Model):
    starId = models.IntegerField(default=0)
    albumId = models.IntegerField(default=0)
    cover = models.CharField(max_length=100, null=True)
    imageListFile = models.CharField(max_length=100, null=True)
    pictureCnt = models.IntegerField(default=0, null=True)
    publishDate = models.DateField(null=True)
    des = models.TextField(null=True)
    company = models.CharField(max_length=30, null=True)
    termID = models.PositiveIntegerField(null=True)
    lastModified = models.DateField(default=timezone.now)


class Star(models.Model):
    starId = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    birthday = models.CharField(max_length=20, null=True)
    cover = models.URLField(default=None, null=True)
    threeD = models.CharField(max_length=15, null=True)
    height = models.IntegerField(default=None, null=True)
    weight = models.FloatField(default=None, null=True)
    hobby = models.CharField(max_length=40, null=True)
    birthPlace = models.CharField(max_length=15, default="", null=True)
    description = models.CharField(max_length=500, default="", null=True)
    tag = models.CharField(max_length=50, default="", null=True)
    lastModified = models.DateField(default=timezone.now)


class Tags(models.Model):
    tagName = models.CharField(max_length=15)
    tagID = models.IntegerField()
    tagTypeName = models.CharField(max_length=50)
    tagTypeID = models.IntegerField()
    albumID = models.TextField()













