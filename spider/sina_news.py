# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:59:38 2017

@author: dianjoy
"""

import urllib.request
import re

data = urllib.request.urlopen('http://news.sina.com.cn/').read().decode('utf-8', 'ignore')

par = '<a target="_blank" href="(http://news.sina.com.cn[^\s].*?)">'
url_list = re.compile(par).findall(data)

for this_url in url_list:
    file = "D:/Agan/spider/weiwei/sinanews/" + str(url_list.index(this_url)+1) + ".html"
    print("第" + str(url_list.index(this_url)+1) +"次爬取")
    try:
        urllib.request.urlretrieve(this_url, file)
        print('--成功--')
    except urllib.request.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
