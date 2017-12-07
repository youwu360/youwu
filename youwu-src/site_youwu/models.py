from django.db import models
from datetime import datetime
from django.utils import timezone


# Create your models here.


class album(models.Model):
    name = models.CharField(max_length = 100)
    starName = models.CharField(max_length = 50)
    starID = models.IntegerField()
    picUrl = models.TextField()
    tag = models.CharField(max_length = 50)
    pictureCnt = models.IntegerField()
    publishDate = models.CharField(max_length=15)
    cover = models.URLField()
    des = models.TextField()
    company = models.CharField(max_length = 30)
    termID = models.PositiveIntegerField()   #第几期
    lastModified = models.DateField()




class star(models.Model):
    name = models.CharField(max_length = 50)  #个人名字
    birthday = models.CharField(max_length = 20) #生日
    threeD = models.CharField(max_length = 15)  #三维
    hobby = models.CharField(max_length = 40)  #兴趣爱好
    wordPlace = models.CharField(max_length = 15)  #所在地
    albumID = models.CharField(max_length =300)  #专辑id 逗号隔开
    des = models.TextField()   #个人描述
    tag = models.CharField(max_length = 50)   #个人标签
    cover = models.URLField()  #个人封面
    lastModified = models.DateField(default=timezone.now)

















