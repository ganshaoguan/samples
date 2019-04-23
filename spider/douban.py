# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 15:45:45 2017
爬取豆瓣阅读内容提供方列表
url = 'https://read.douban.com/provider/all'

@author: Alvin Gan
"""

import urllib.request
import re


url = 'https://read.douban.com/provider/all'
data = urllib.request.urlopen(url).read().decode('utf-8')  # 获取链接内容，并读取内容，以utf8格式

par = '<div class="name">(.*?)</div>'   # 正则表达式,出版社信息记录格式为： <div class="name">百花洲文艺出版社</div>
result = re.compile(par).findall(data)  # 查找所有满足条件的内容

f = open("D:\\Agan\\spider\\urllib实战.txt", 'w')   # 存储到本地
for res in result:
    f.write(res + '\n')
    print(len(res))
f.close()
print('Done')
