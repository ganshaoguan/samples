# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 11:16:25 2017

@author: Alvin Gan
"""
'''
import threading
import time
import queue

# 无线程

def a():
    for i in range(0, 10):
        print('我是a')
        
def b():
    for i in range(0, 10):
        print('我是b')
        
a()
b()

# 单线程的结果是顺序执行的，即按照代码顺序依次执行完a()然后才会执行b()


time.sleep(5)   # 程序暂停5秒


# 下面是线程的操作

class A(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        for i in range(0, 10):
            print('我是线程A')
            
            
class B(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        for i in range(0, 10):
            print('我是线程B')
            
t1 = A()
t1.start()
t2 = B()
t2.start()


# 多线程是同步执行的
# 队列的概念，依次进入，先进先出，后进后出

time.sleep(5)

a = queue.Queue()   # 此时a就是一个队列
a.put('python')    # 向队列a中添加元素 python
a.task_done()   # 表示添加元素的任务结束
a.put('php')
a.task_done()

print(a.get())  # 输出a的元素，先进先出，后进后出
print(a.get()) 

'''


'''

根据多线程和队列我们可以这样操作，建立两个线程，一个用来爬取主页里的段子链接，链接，依次写入队列，
另一个根据队列依次根据段子链接将段子爬取到本地，

尝试对糗百文字部分进行试验
'''

'''
# 首先尝试一下单线程
import re
import urllib.request
import time


#headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0')
#opener = urllib.request.build_opener()
#opener.addheaders = [headers]
#urllib.request.install_opener(opener)

# 获取段子的链接
def get_url(url, proxy_addr):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0')
    
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    try:
        data = urllib.request.urlopen(req).read().decode('utf-8')
        par = '<a href="(/article/\w*?)" target="_blank" class="contentHerf" onclick'
        article_list = re.compile(par).findall(data)
        article_url = []
        for m in article_list:
            link = 'https://www.qiushibaike.com' + m
            article_url.append(link)
        return article_url
    except urllib.request.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
    except Exception as e:
        print(e)
    


# 获取段子里的内容
def get_content(url, proxy_addr):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0')
    
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    try:
        data = urllib.request.urlopen(req).read().decode('utf-8')
        par_name = '<h2>(.*?)</h2>'
        par_content = '<div class="content">(.*?)</div>'
        pre_name = re.search(par_name, data)
        pre_content = re.search(par_content, data, re.S)
        name = pre_name.group(1).replace('\n', '').replace('<br/>', '')
        content = pre_content.group(1).replace('\n', '').replace('<br/>', '')
        return name, content
    except urllib.request.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
    except Exception as e:
        print(e)



if __name__ == '__main__':
    proxy = '127.0.0.1:8888'
    f = open('D:/Agan/spider/weiwei/qiubai/danxiancheng.txt', 'a')
    for i in range(1, 10):
        time.sleep(2)
        url = 'https://www.qiushibaike.com/text/page/%s/' % str(i)
        print('正在爬取第%s页内容' %str(i))
        url_list = get_url(url, proxy)
        if len(url_list) == 0:
            print('本页爬取失败')
            continue
        for m in range(0, len(url_list)):
            time.sleep(1)
            print('正在爬取第%s页第%s个段子' % (str(i), str(m+1)))
            result = get_content(url_list[m], proxy)
            f.write(result[0] + ' 说：\n\n')
            f.write(result[1] + '\n\n\n')
    f.close()
    print('Task Done')



# 可以看出，单线程是运行完爬链接的任务，再运运行爬段子的任务

'''
'''
正在爬取第1页内容
正在爬取第1页第1个段子
正在爬取第1页第2个段子
正在爬取第1页第3个段子
正在爬取第1页第4个段子
正在爬取第1页第5个段子
正在爬取第1页第6个段子
正在爬取第1页第7个段子
正在爬取第1页第8个段子
正在爬取第1页第9个段子
正在爬取第1页第10个段子
……
'''





# 尝试一下多线程

import urllib.request
import re
import threading
import queue
import time

urlqueue = queue.Queue()

class get_url(threading.Thread):
    def __init__(self, url, page, proxy_addr, urlqueue):
        threading.Thread.__init__(self)
        self.url = url
        self.page = page
        self.proxy_addr = proxy_addr
        self.urlqueue = urlqueue
        
    def run(self):
        for i in range(1, self.page):
            url = self.url + str(i)
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0')
            proxy = urllib.request.ProxyHandler({'http': self.proxy_addr})
            opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
            urllib.request.install_opener(opener)
            try:
                data = urllib.request.urlopen(req).read().decode('utf-8')
                par = '<a href="(/article/\w*?)" target="_blank" class="contentHerf" onclick'
                article_list = re.compile(par).findall(data)
                for m in range(0, len(article_list)):
                    link = 'https://www.qiushibaike.com' + article_list[m]
                    self.urlqueue.put(link)
                    self.urlqueue.task_done()
                    print('第%s页第%s个链接入队列' % (str(i), str(m+1)))
            except urllib.request.URLError as e:
                if hasattr(e, 'code'):
                    print(e.code)
                if hasattr(e, 'reason'):
                    print(e.reason)
            except Exception as e:
                print(e)



class get_content(threading.Thread):
    def __init__(self, proxy_addr, urlqueue):
        threading.Thread.__init__(self)
        self.proxy_addr = proxy_addr
        self.urlqueue = urlqueue
        
    def run(self):
        i = 1
        while True:
            url = self.urlqueue.get()
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0')
            proxy = urllib.request.ProxyHandler({'http': self.proxy_addr})
            opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
            urllib.request.install_opener(opener)
            try:
                f = open('D:/Agan/spider/weiwei/qiubai/duoxiancheng.txt', 'a')
                data = urllib.request.urlopen(req).read().decode('utf-8')
                par_name = '<h2>(.*?)</h2>'
                par_content = '<div class="content">(.*?)</div>'
                pre_name = re.search(par_name, data)
                pre_content = re.search(par_content, data, re.S)
                name = pre_name.group(1).replace('\n', '').replace('<br/>', '')
                content = pre_content.group(1).replace('\n', '').replace('<br/>', '')
                f.write(name + ' 说：\n\n')
                f.write(content + '\n\n\n')
                f.close()
                print('这是第%s个网页' % str(i))
                i += 1
            except urllib.request.URLError as e:
                if hasattr(e, 'code'):
                    print(e.code)
                if hasattr(e, 'reason'):
                    print(e.reason)
            except Exception as e:
                print(e)



# 创建第三个线程，判断程序是否结束
class is_over(threading.Thread):
    def __init__(self, urlqueue):
        threading.Thread.__init__(self)
        self.urlqueue = urlqueue
        
    def run(self):
        while True:
            time.sleep(10)
            if (self.urlqueue.empty()):
                print('程序结束')
                exit()
        
        
        

        
proxy = '127.0.0.1:8888'
url = 'https://www.qiushibaike.com/text/page/'

one = get_url(url, 3, proxy, urlqueue)
one.start()

two = get_content(proxy, urlqueue)
two.start()

three = is_over(urlqueue)
three.start()
        
        
