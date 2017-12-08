import os
import urllib.request

url = "http://n.sinaimg.cn/news/transform/w1000h500/20171206/PdPG-fypikwu3068310.jpg"

def get_img_path(url):
    # url 转换文件路径的函数
    base_dir=os.getcwd()
    full_name = os.path.join(base_dir, url.replace("http://", ""))
    file_dir = os.path.split(full_name)[0]
    file_name = os.path.split(full_name)[1]
    return {"full_name": full_name, "file_dir": file_dir, "file_name": file_name}

def get_img(url):
    path = get_img_path(url)
    # print(path)
    if not os.path.exists(path["file_dir"]):
        os.makedirs(path["file_dir"])
    urllib.request.urlretrieve(url, path["full_name"])

get_img(url)
