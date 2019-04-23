# -*- coding:utf-8 -*-
'''
@author: Alvin Gan
爬一爬 "顶点小说" 网的 《我的盗墓生涯》

'''

import urllib.request
import re
from lxml import etree
from datetime import datetime
import time
import random
import socket

print(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S',))   # 打印当前时间
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}

# 设置代理ip，使用的fiddler，应该也可以做代理吧
proxy = urllib.request.ProxyHandler({'http': '127.0.0.1:8888'})
opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
urllib.request.install_opener(opener)


# 获取数据函数
def get_data(url):
    try:
        print('此时在Request')
        res = urllib.request.Request(url, headers = headers)  # 模拟浏览器
        print('此时在urlopen')
        html = urllib.request.urlopen(res, timeout= 8)
        print('此时在read')
        data = html.read().decode('gbk', 'ignore')
        return data
    except urllib.request.URLError as e:
        if isinstance(e.reason, socket.timeout):
            try:
                print('请求超时，正在重新尝试')
                res = urllib.request.Request(url, headers=headers)  # 模拟浏览器
                html = urllib.request.urlopen(res, timeout=8)
                data = html.read().decode('gbk', 'ignore')
                return data
            except Exception as ee:
                print('重新请求失败')
                print(ee)
                return None
        else:
            print(e)
            return None
    except Exception as e:
        print('Error: %s' % str(e))
        return None


# 整理数据的函数，使用的xpath解析的网页数据,返回章节标题、文章内容、下一章网址三个元素组成的元组 ([title], [next_url], 'content')
def get_content(data):
    result = etree.HTML(data)
    # 正则需要替换掉的东西
    pat = r'''\r|\n|\xa0|</p>|<script language="javascript" type="text/javascript" src="/js/neirongye300-250.js"></script>'''
    title = result.xpath('//div[@class="bookname"]/h1/text()')
    next_url = result.xpath('//div[@class="bottem1"]/a[text()="下一章"]/@href')
    content2 = result.xpath('//div[@id="content"]/text()')
    content1 = " ".join(map(str, content2))
    content = re.sub(pat, " ", content1)
    return title, next_url, content



# 链接是由前半部分的固定链接加上后半部分的页码链接构成https://www.booktxt.net，  和 /0_693/176376.html
if __name__ == '__main__':
    end_url = '/0_693/'  # 当下一章网址为这个值的时候说明也就到最后一章了，程序结束
    url = 'https://www.booktxt.net/0_693/176570.html'  # 第一章的url
    with open('D:/Agan/spider/我的盗墓生涯.txt', 'a', encoding= 'utf-8') as f:
        while True:
            data = get_data(url)
            if data is None:
                print('get_data数据为空，跳过，进行下一条')
                continue
            else:
                result = get_content(data)
                if result[1][0] == end_url:   # get_content返回的是一个元组，next_url排在第1位
                    print(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S', ))  # 打印当前时间
                    print("This is the last chapter, process is end!")
                    break
                else:
                    title = result[0][0]
                    content = result[2]
                    print(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S', ))  # 打印当前时间
                    print("正在写入：%s" % title)
                    print("本章链接是: %s" % url)
                    f.write(str(title) + '\n' + content + '\n\n')  # 写入到文件，章节之间空两行，标题与内容之间空一行
                    url = 'https://www.booktxt.net' + result[1][0]   # 重新构造下一章的url地址
                    time.sleep(random.randint(1,3))
        f.close()


print(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S',))   # 打印当前时间
