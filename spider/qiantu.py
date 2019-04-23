# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 17:49:21 2017

@author: dianjoy
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 20:28:54 2017

@author: Alvin Gan
"""

import urllib.request
import re
import time
from random import choice

headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36')
opener = urllib.request.build_opener()
opener.addheaders = [headers]
urllib.request.install_opener(opener)

'''
# 使用代理ip爬数据

def use_proxy(url, proxy_addr):
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    try:
        data = urllib.request.urlopen(url, timeout=10).read().decode('utf-8', 'ignore')
    except urllib.request.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
    return data

proxy_addr = ['113.218.216.118:8888', '219.138.58.146:3128', '112.114.78.217:8118']

ori_url = 'http://www.58pic.com/c/5524287?page='

for i in range(1, 4):  # 获取钱三页数据  
    url = ori_url + str(i)
    proxy = choice(proxy_addr)
    data = use_proxy(url, proxy)
    print('正在爬去第%s页数据' % str(i))
    par = '"(http://pic.qiantucdn.com/58pic/.*?\.jpg)!'
    image_url = re.compile(par).findall(data)
    print(image_url)
    for m in range(0, len(image_url)):
        file = 'E:/Alvin/spyder/qiantu/第%s页第%s张.jpg' % (str(i), str(m + 1))
        print('正在爬取第%s页第%s张' % (str(i),str(m + 1)))
        urllib.request.urlretrieve(image_url[m], filename= file)
        time.sleep(2)
        
print('爬取工作已经完成')

''' 

# 使用代理ip爬取总是出错，使用自己的ip试试

def use_proxy(url):
    try:
        data = urllib.request.urlopen(url, timeout=10).read().decode('utf-8', 'ignore')
    except urllib.request.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
    return data


ori_url = 'http://www.58pic.com/c/5524287?page='   # url可以根据自身实际需要来修改，注意观察url的规律

for i in range(1, 3):  # 获取前两页数据  
    url = ori_url + str(i)
    data = use_proxy(url)
    print('正在爬去第%s页数据' % str(i))
    par = '"(http://pic.qiantucdn.com/58pic/.*?\.jpg)!'
    image_url = re.compile(par).findall(data)
    for m in range(0, len(image_url)):
        file = 'D:/Agan/spider/weiwei/qiantu/第' + str(i) + '页' + str(m+1) + '.jpg'
        print('正在爬取第%s页第%s张' % (str(i),str(m + 1)))
        urllib.request.urlretrieve(image_url[m], file)
        time.sleep(2)
        
print('爬取工作已经完成')
