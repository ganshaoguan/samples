# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:59:22 2017

@author: Alvin Gan
"""

import urllib.request

url = 'http://blog.csdn.net/weiwei_pig/article/details/54647680'
header = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36")
opener = urllib.request.build_opener()
opener.addheaders = [header]

data = opener.open(url).read()
f = open("D:/Agan/spider/weiwei/4.html", "wb")
f.write(data)
f.close()
