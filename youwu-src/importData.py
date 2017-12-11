#coding=utf-8
import urllib.request
from bs4 import BeautifulSoup
import os
import gzip
import random
import string
import multiprocessing
import datetime



url= "https://www.meitulu.com/item/4208.html"

def getPage(url):
#获取网页
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20170201 Firefox/3.5.6'}
    req = urllib.request.Request(url=url, headers=headers)
    res=urllib.request.urlopen(req)
    page = res.read()

    #判断是否压缩
    if res.info().get('Content-Encoding')=='gzip':
        page=gzip.decompress(page)
    soup = BeautifulSoup(page,"html.parser")
    #print(soup)
    return soup


#getPage(url)


def getAttrByNum(page_num):

    page_url="https://www.meitulu.com/item/"+ str(page_num) + ".html"
    soup = getPage(page_url)

    name=soup.head.title.string.split('_')[0]

    count=int(soup.find_all('p')[2].string.split(' ')[1])

    publish_time = soup.find_all('p')[5].string.split(' ')[1]

    company = name.split(']')[0].split('[')[1]

    star_name = name.split(' ')[2]

    termID = int(name.split(' ')[1].split('.')[1])

    tags=list()



    tag = soup.find('div',"fenxiang_l")

    for a in tag:
        tags.append(a.string)
    #print(tags[1:])


    url_list = str()
    for i in range(1,count+1):
        url="http://mtl.ttsqgs.com/images/img/"+ str(page_num) +"/" + str(i) + ".jpg"
        url_list =  url_list +','+url

    """
    bad_list=["BOMB.tv","WPB-net","DGC","4K-","Web","Shock","BWH","Graphis","WBGC","UXING","V女郎","AISS","misty","Misty","digital books","Ys Web","Wanibooks","Minisuka","Sabra","Beautyleg"," Digital Books","NS Eyes","动感小站","image.tv","RQ-STAR套图","For-side","TyingArt","VYJ",]
    for item in bad_list:
        if item in str(name):
            url_list=list()
            print(item)
            break
    
    """

    attr={
        "name":name,
        "starName":star_name,
        "starID":0,
        "picUrl":url_list,
        "tag":tags[1:],
        "pictureCnt":count,
        "publishDate":publish_time,
        "cover":"http://ww2.sinaimg.cn/large/0060lm7Tly1flvnxn2erfj30rs0xcmzb.jpg",
        "des":"如此婀娜，如此柔情，当她回眸的瞬间，心跳似乎静止，被那迷醉的神情深深吸引。这人间尤物，便是尤果伊莉娜。混血儿的模样总是令人特别喜欢，高挺的鼻梁，魅惑的双眼，完美的身材一定是得到了上帝的特别关爱。当她披着白色的衬衫，站在墙角，你的眼睛一定会被牢牢锁定无可转移。她趴在桌子上，翘起高高的美臀，像猫咪一样伸着懒腰，皮肤在补光灯下发出晶莹剔透的光芒，女神二字无可厚非。她又来到窗边，侧颜秒杀一切，当黑色的蕾丝绽放的时候，我竟有些不相信我所看见的一切。",
        "company":company,
        "termID":termID,
        "lastModified":datetime.datetime.now().strftime('%Y-%m-%d'),
    }
    return attr


file= open('data.txt','w')
for num in range(8000,10000):
    print(num)
    try:
        res = getAttrByNum(num)
        print(str(res))
        file.write(str(res))
        file.write('\n')
    except:
        continue


file.close()




