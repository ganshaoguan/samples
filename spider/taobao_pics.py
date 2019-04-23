# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 11:09:42 2017

@author: Alvin Gan
"""

import urllib.request
import re
from random import choice
import time


headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0')
opener = urllib.request.build_opener()
opener.addheaders = [headers]
urllib.request.install_opener(opener)


def use_proxy(url, proxy_addr):
    proxy = urllib.request.ProxyHandler({'http':proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read().decode('utf-8')
    return data


proxy = ['49.69.220.190:8118', '122.114.206.211:808','222.76.187.202:8118','219.138.58.107:3128']  # 代理ip池
name = '书包'
keyword = urllib.request.quote(name)
for i in range(0, 3):
    url = 'https://s.taobao.com/search?q=%s&s=%s' % (keyword, str(i*44))
    proxy_addr = choice(proxy)
    try:
        data = use_proxy(url, proxy_addr)
        time.sleep(10)
    except urllib.request.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
    par = 'pic_url":"(.*?)"'
    image_url = re.compile(par).findall(data)
    print("正在爬取第%s页内容" % str(i+1))
    for m in range(0, len(image_url)):
        every_image_url = 'http:' + image_url[m]
        print("正在爬取第%s页第%s张图片" % (str(i+1), str(m + 1)))
        file = "D:/Agan/spider/weiwei/taobao/第"+str(i+1) + "页第" + str(m+1)+"张图片.jpg"
        try:
            urllib.request.urlretrieve(every_image_url,file)
            time.sleep(5)
        except urllib.request.URLError as e:
            if hasattr(e, 'code'):
                print(e.code)
            if hasattr(e, 'reason'):
                print(e.reason)
        
print("爬取完毕")
