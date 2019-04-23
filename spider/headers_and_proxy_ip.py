# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 15:36:09 2017

@author: Alvin Gan
"""

import urllib.request
# import re


'''

# 添加报头
headers = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36")
opener = urllib.request.build_opener()   # 创建opener对象
opener.addheaders = [headers]   # 添加报头
urllib.request.install_opener(opener)   # 设置为全局

# 使用代理ip

def use_proxy(url, proxy_addr):
    proxy = urllib.request.ProxyHandler({'http':proxy_addr})  # 设置代理ip地址
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)  
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read().decode('utf-8')
    return data


'''




# 添加报头和使用代理ip放置在同一个函数下面

def use_proxy(url, proxy_addr):
    req = urllib.request.Request(url)   # 创建一个Request对象
    # 使用对象的add_header方法添加报头，参数为  key,value的格式
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36')
    
    # 设置代理ip
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    
    data = urllib.request.urlopen(req).read().decode('utf-8')
    return data
