# /user/bin/python3
# -*-coding:utf-8 -*-

'''
@author = 'Alvin Gan'

'''

import urllib.request

keyword = input('Please input you want to search:')
keyword = urllib.request.quote(keyword)

url = 'http://www.baidu.com/s?wd=%s' % keyword

req = urllib.request.Request(url)

data = urllib.request.urlopen(req).read()

f = open('D:/Agan/spider/weiwei/2.html', 'wb')
f.write(data)
f.close()
