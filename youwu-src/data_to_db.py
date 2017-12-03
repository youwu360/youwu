import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "basics.settings")
import django
django.setup()
from site_youwu.models import ablum
from site_youwu.models import star
from  datetime import datetime


def ablum_data():    #从文件中导入原始数据
    file = open('data.txt')
    for line in file:
        line = eval(line)
        print(line['name'])
        ablum.objects.create(
            name=line['name'],
            starName = line['starName'],
            starID = line['starID'],
            picUrl = line['picUrl'],
            tag = line['tag'],
            pictureCnt = line['pictureCnt'],
            publishDate = line['publishDate'],
            cover = line['cover'],
            des = line['des'],
            company = line['company'],
            termID = line['termID'],
            lastModified = line['lastModified']
        )
    file.close()

#ablum_data()

"""
def ablum_data_change():  #未调通
    file = open('data.txt')
    for line in file:
        line = eval(line)
        ablum.objects.filter(name=line['name']).update(picUrl=line['picUrl'])
        print(line['name'])
        print(line['picUrl'])

"""

"""
    name = models.CharField(max_length = 50)  #个人名字
    birthday = models.CharField(max_length = 20) #生日
    threeD = models.CharField(max_length = 15)  #三维
    hobby = models.CharField(max_length = 40)  #兴趣爱好
    wordPlace = models.CharField(max_length = 15)  #所在地
    ablumID = models.CharField(max_length =300)  #专辑id 逗号隔开
    des = models.TextField()   #个人描述
    tag = models.CharField(max_length = 50)   #个人标签
    cover = models.URLField()  #个人封面
    lastModified = models.DateField(default=timezone.now)
"""

def star_data():
    temp = ablum.objects.all().values('name')
    for line in temp:

        line['birthday'] = "1992.08.09"
        line['threeD'] = "90-87-100"
        line['hobby'] = "看书，游泳，购物"
        line['wordPlace'] = "北京"
        line['ablumID'] = ablum.objects.filter(name=line['name']).values('id')[0]["id"]
        line['des'] = "貌美如花；貌美如花；貌美如花；貌美如花；貌美如花；貌美如花；"
        line['tag'] = "镁铝、女神、童颜"
        line['cover'] = "http://www.znns.com/d/file/p/2016-07-26/6a1d7e942857bac80a6f4b3106b8a34d.jpg"
        line['lastModified'] = datetime.now().strftime("%Y-%m-%d")

        star.objects.create(
            name = line['name'],
            birthday = line['birthday'],
            threeD = line['threeD'],
            hobby = line['hobby'],
            wordPlace = line['wordPlace'],
            ablumID = line['ablumID'],
            des = line['des'],
            tag = line['tag'],
            cover = line['cover'],
            lastModified = line['lastModified']
        )

        print(line)

star_data()


