# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 11:06:09 2017

@author: dianjoy
"""

import urllib.request
import urllib.parse

url = 'http://www.iqianyue.com/mypost/'
mydata = urllib.parse.urlencode({
        'name':'agan',
        'pass':'agan'
        }).encode('utf-8')

res = urllib.request.Request(url, mydata)

data = urllib.request.urlopen(res).read()

f = open('D:/Agan/spider/weiwei/3.html', 'wb')
f.write(data)
f.close()
