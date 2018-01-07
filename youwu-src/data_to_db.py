import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "basics.settings")
import django
django.setup()
from site_youwu.models import Album
from site_youwu.models import Star
from site_youwu.models import Tags
from  datetime import datetime
from site_youwu.view_list.view_common import clean_str
import math


def album_data():    #从文件中导入原始数据
    file = open('data.txt')
    for line in file:
        line = eval(line)
        print(line['name'])
        Album.objects.create(
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


"""
def album_data_change():  #未调通
    file = open('data.txt')
    for line in file:
        line = eval(line)
        album.objects.filter(name=line['name']).update(picUrl=line['picUrl'])
        print(line['name'])
        print(line['picUrl'])

"""

"""
    name = models.CharField(max_length = 50)  #个人名字
    birthday = models.CharField(max_length = 20) #生日
    threeD = models.CharField(max_length = 15)  #三维
    hobby = models.CharField(max_length = 40)  #兴趣爱好
    workPlace = models.CharField(max_length = 15)  #所在地
    albumID = models.CharField(max_length =300)  #专辑id 逗号隔开
    des = models.TextField()   #个人描述
    tag = models.CharField(max_length = 50)   #个人标签
    cover = models.URLField()  #个人封面
    lastModified = models.DateField(default=timezone.now)
    
    
"""

def star_data():
    temp = Album.objects.all().values('starName').distinct()   #获取所有明星的名字
    for line in temp:

        line['birthday'] = "1992.08.09"
        line['threeD'] = "90-87-100"
        line['hobby'] = "看书，游泳，购物"
        line['workPlace'] = "北京"
        line['albumID'] = Album.objects.filter(starName=line['starName']).values('id')[0]["id"]    #temp
        line['des'] = "貌美如花；貌美如花；貌美如花；貌美如花；貌美如花；貌美如花；"
        line['tag'] = "镁铝、女神、童颜"
        line['cover'] = "http://www.znns.com/d/file/p/2016-07-26/6a1d7e942857bac80a6f4b3106b8a34d.jpg"
        line['lastModified'] = datetime.now().strftime("%Y-%m-%d")

        Star.objects.create(
            name = line['starName'],
            birthday = line['birthday'],
            threeD = line['threeD'],
            hobby = line['hobby'],
            workPlace = line['workPlace'],
            albumID = line['albumID'],
            des = line['des'],
            tag = line['tag'],
            cover = line['cover'],
            lastModified = line['lastModified']
        )

        print(line)


def set_album_starID():
    album_id_starName = Album.objects.all().values("id", "starName")
    for line in album_id_starName:
        album_star_name = line['starName']
        album_id = line['id']

        print(album_star_name)
        star_id = Star.objects.filter(name=album_star_name).values('id')[0]['id']     #temp
        Album.objects.filter(id=album_id).update(starID = star_id)


def set_temp_url_list():   #修改样例图片
    url_sample = "http://ww4.sinaimg.cn/large/0060lm7Tly1fm5qfvzygej30xc1jngqh.jpg,http://ww2.sinaimg.cn/large/0060lm7Tly1fm5qfy411uj30xc1jnwjo.jpg,http://ww2.sinaimg.cn/large/0060lm7Tly1fm5qfzol9gj30xc1jnn3m.jpg,http://ww3.sinaimg.cn/large/0060lm7Tly1fm5qfzvyumj30xc1jndlr.jpg,http://ww2.sinaimg.cn/large/0060lm7Tly1fm5qg1szsqj30xc1jnwka.jpg,http://ww1.sinaimg.cn/large/0060lm7Tly1fm5qg399ngj30xc1jntev.jpg,http://ww1.sinaimg.cn/large/0060lm7Tly1fm5qg4ahw5j30xc1jn44g.jpg,http://ww1.sinaimg.cn/large/0060lm7Tly1fm5qg6o7ixj30xc1jntdu.jpg,http://ww1.sinaimg.cn/large/0060lm7Tly1fm5qg7jt4ej30xc1jndlr.jpg,http://ww2.sinaimg.cn/large/0060lm7Tly1fm5qg8ozkxj30xc1jnn1l.jpg,http://ww1.sinaimg.cn/large/0060lm7Tly1fm5qgcejofj30xc1jntdq.jpg,http://ww1.sinaimg.cn/large/0060lm7Tly1fm5qgd6ox4j30xc1jntdw.jpg,http://ww3.sinaimg.cn/large/0060lm7Tly1fm5qgj6i9pj30xc1jn43l.jpg,http://ww4.sinaimg.cn/large/0060lm7Tly1fm5qgl0996j30xc1jnjxm.jpg,http://ww3.sinaimg.cn/large/0060lm7Tly1fm5qglj1dtj30xc1jntdx.jpg,http://ww3.sinaimg.cn/large/0060lm7Tly1fm5qglq4t5j30xc1jnn56.jpg,http://ww4.sinaimg.cn/large/0060lm7Tly1fm5qgmkbdrj30xc1jn78f.jpg,http://ww4.sinaimg.cn/large/0060lm7Tly1fm5qgndr3pj30xc1jnn25.jpg,http://ww2.sinaimg.cn/large/0060lm7Tly1fm5qgp4hzhj30xc1jnjv5.jpg,http://ww2.sinaimg.cn/large/0060lm7Tly1fm5qgrer9mj30xc1jnte7.jpg"
    Album.objects.all().update(picUrl = url_sample)


def get_all_album_tag():
    temp = Album.objects.all().values("tag")
    tag_list = list()
    for a in temp:
        #print("a:",a)
        a_list = clean_str(a["tag"]).split(",")
        print("a_list", a_list,type(a_list))

        for b in a_list:
                if len(b) > 2 and b not in tag_list:
                    tag_list.append(b)
    print(tag_list)
    print(len(tag_list))



def get_type_dict():
    tag_list = ['学生妹', '丝袜诱惑', '长筒袜', '美少女', '丝袜美女', '网络红人', '足球宝贝', 'ShowGirl', '丁字裤', '大尺度', '兔女郎', 'COSPLAY', '私房照', '丝袜美腿', '高跟鞋', '透视装', '萌妹操服', '日本美女', 'COSER', '人体艺术', '台湾美女', '圣诞美女', '肉丝袜']
    tag_type_list = ['服饰','国家','身材','身份','地方']
    i = 1
    j = 5
    res =list()

    for a in tag_list:
        temp = dict()
        k = math.ceil(i/j)
        temp["tagName"] = a
        temp["tagId"] = i
        temp["tagTypeId"] = k
        temp["tagTypeName"] = tag_type_list[k-1]
        #print(temp)
        res.append(temp)

        #list.append('{"tagName": "',a , '", "tagID": ',i , ', "tagType": ',k ,'"tagTypeID": "',tag_type_list[k-1],'},')
        i = i + 1
    return res



def set_tag_data():
    data = get_type_dict()
    print(data)
    for line in data:
        albumid = ""
        temp = Album.objects.all().values("albumId")[1:200]
        for a in temp:
            albumid = albumid + "," + str(a["albumId"])
        albumid = albumid.strip(",")

        Tags.objects.create(
            tagName = line["tagName"],
            tagId = line["tagId"],
            tagTypeName = line["tagTypeName"],
            tagTypeId = line["tagTypeId"],
            albumId = albumid
        )


def set_star_cover():
    cover = "http://www.znns.com/d/file/p/2016-07-26/6a1d7e942857bac80a6f4b3106b8a34d.jpg"
    Star.objects.all().update(cover = cover)



"""
album_data()
star_data()
set_album_starID()
set_temp_url_list()
set_tag_data()
set_star_cover()
set_tag_data()
"""


def set_album_list():
    data = Album.objects.all().values("albumId")
    album_lsit = []
    for line in data:
        album_lsit.append(line["albumId"])
    Tags.objects.all().update(albumIdList = str(album_lsit))
set_album_list()
