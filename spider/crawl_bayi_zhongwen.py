# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 08:28:35 2018

@author: Alvin Gan
"""

import urllib.request
import re
from lxml import etree
import time

print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))

# 模拟浏览器
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}

# 代理ip，使用的fiddler，应该也可以做代理吧
proxy = urllib.request.ProxyHandler({'http':'127.0.0.1:8888'})
opener2 = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
urllib.request.install_opener(opener2)

def get_data(url):
    try:
        data1 = urllib.request.Request(url, headers = headers) # 模拟浏览器
        data = urllib.request.urlopen(data1).read().decode('gbk')
        return data
    except urllib.request.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
    except Exception as e:
        print('Error:%s' % str(e))


def get_content(data):
    result = etree.HTML(data)
    title = result.xpath('//div[@class="bookname"]/h1/text()')
    next_url = result.xpath('//div[@class="bottem1"]/a[text()="下一章"]/@href')
    content1 = result.xpath('//div[@id="content"]/text()')
    content2 = ''
    for i in range(0, len(content1)):
        content2 = content2 + str(content1[i])
    par = '''[\xa0|Ｗ|８１ＺＷ．ＣＯＭ|八一中文网|]'''
    content = re.sub(par, '', content2)
    return title, content, next_url



if __name__ == '__main__':
    url = 'https://www.zwdu.com/book/20227/5755384.html'
    end_url = '/book/20227/'   # 最后一章的下一章是本书目录，返回的是这个链接
    f = open("E:/Alvin/spyder/女总裁的全能兵王.txt", 'a')
    while True:
        data = get_data(url)
        a = get_content(data)
        if a[2] == end_url:
            print("已到最后一章，任务结束!")
            break
        title = a[0][0]
        content = a[1]
        print("正在写入:%s" % title)
        print("本章链接是:%s" % url)
        f.write(str(title) + '\n' + content  + '\n\n')
        url = 'https://www.zwdu.com' + a[2][0]
    f.close()
    
print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))











# 没错，就是爬了个小说
