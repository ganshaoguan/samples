# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 17:36:25 2017

http://weixin.sogou.com

@author: Alvin G
"""

import urllib.request
import re
import time

# 使用代理ip
def use_proxy(url, proxy_addr):
    # 设置全局报头
    req = urllib.request.Request(url)     # 创建request对象
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0')
    # 设置代理ip
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    try:
        data = urllib.request.urlopen(req).read().decode('utf-8')
        par = '<a target="_blank" href="(http.*?)"'
        url_list = re.compile(par).findall(data)
        return url_list
    except urllib.request.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
    except Exception as e:
        print(e)
        
# 分析微信文章的url发现，page表示页数， type = 2表示搜索文章 ，query为搜索关键词
# 爬虫返回的链接中带有无效字符   amp;   需要将无效字符替换掉

proxy = '127.0.0.1:8888'  # 
key = input("Please input you want to search:")
keyword = urllib.request.quote(key)

for i in range(0, 3):
    url = 'http://weixin.sogou.com/weixin?query=' + keyword + '&page=' + str(i) + '&type=2'
    url_list = use_proxy(url, proxy)
    time.sleep(10)
    print("正在爬取第%s页数据" % str(i+1))
    if len(url_list) == 0:
        print("第%s页爬取失败" % str(i+1))
        continue
    for m in range(0, len(url_list)):
        text_url = url_list[m].replace("amp;","")
        file = "D:/Agan/spider/weiwei/webchat/第" + str(i + 1) +"页第" + str(m + 1) + "篇文章.html"
        try:
            print("正在爬取第%s页%s篇文章" % (str(i+1), str(m+1)))
            urllib.request.urlretrieve(text_url, file)
            time.sleep(5)
        except Exception as e:
            print(e)

print("爬取完毕")
