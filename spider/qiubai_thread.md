这两天看了看多线程爬虫，拿来爬糗百试试


```python
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 11:28:34 2017

@author: dianjoy
目测需要写3个线程
1 爬取段子链接
2 根据段子链接爬取正文并存储到本地
3 判断程序是否完成
"""

import re
import urllib.request
import urllib.error
import threading
import queue
import time

urlqueue = queue.Queue()
urllist = []

# 添加报头
headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36')
opener = urllib.request.build_opener()
opener.addheaders = [headers]
urllib.request.install_opener(opener)

# 使用代理ip地址

# def use_proxy(proxy_addr, url):
def use_proxy(url):
    try:
#        proxy = urllib.request.ProxyHandler({'http':proxy_addr})
#        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
#        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(url).read().decode('utf-8')
        return data
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
    except Exception as e:
        print("Exception:%s" % str(e))
        

# 线程1 获取对应网址并处理为真是网址

class geturl(threading.Thread):
    # def __init__(self, pagestart, pageend, proxy, urlqueue):
    def __init__(self, pagestart, pageend, urlqueue):
        threading.Thread.__init__(self)
        self.pagestart = pagestart
        self.pageend = pageend
        # self.proxy = proxy
        self.urlqueue = urlqueue
        
    def run(self):
        print("一共%s页链接" % str(self.pageend - self.pagestart + 1))
        for page in range(self.pagestart, self.pageend + 1):
            print("正在抓取第%s页链接" % str(page))
            url = "https://www.qiushibaike.com/text/page/" + str(page) + "/"
            # data1 = use_proxy(self.proxy, url)
            data1 = use_proxy(url)
            part1 = r'''<a href="(.*?)" target="_blank" class="contentHerf" onclick="_hmt.push'''   # 每篇文章的id
            result = re.compile(part1).findall(data1)   # 返回一个列表值，like ["/article/119521405", "/article/11952140"]
            urllist.append(result)  # 将result列表作为一个元素添加到urllist列表里去
        print("共抓取到%s页" % str(len(urllist)))
        for i in range(0, len(urllist)):
            time.sleep(5)  # 稍作休息
            for j in range(0, len(urllist[i])):
                try:
                    url = urllist[i][j]
                    url = "https://www.qiushibaike.com" + url   # 构造完整的url链接 like   https://www.qiushibaike.com/article/119677706
                    print("第" + str(i) + "i" + str(j) + "j次入队")
                    self.urlqueue.put(url)
                    self.urlqueue.task_done()
                except urllib.error.URLError as e:
                    if hasattr(e, "code"):
                        print(e.code)
                    if hasattr(e, "reason"):
                        print(e.reason)
                    time.sleep(5)
                except Exception as e:
                    print("Exception:%s" % str(e))
                    time.sleep(1)
                    
# 线程2,爬取正文                    
class getcontent(threading.Thread):
    # def __init__(self, urlqueue, proxy):
    def __init__(self, urlqueue):
        threading.Thread.__init__(self)
        self.urlqueue = urlqueue
        # self.proxy = proxy
    
    def run(self):
        i = 1
        while(True):
            try:
                url = self.urlqueue.get()
                # data = use_proxy(self.proxy, url)
                data = use_proxy(url)
                name_part = r'''<a href="/users/\w*?/" target="_blank" title=".*?">.*?<h2>(.*?)</h2>'''
                content_part = r'''<div class="content">(.*?)</div>'''
                name1 = re.compile(name_part, re.S).findall(data)
                content1 = re.compile(content_part, re.S).findall(data)
                name = re.sub(r'''[\s|\n|\r|<\br>|" "]''',"",name1[0])  # 去掉空格，换行符等
                content = re.sub(r'''[\s|\n|\r|<\br>|" "|b/]''',"",content1[0])
                print("第%s个网页处理" % str(i))
                with open("D:/Agan/spider/qiubai/qiubai.txt", "a", encoding="gbk", errors= "ignore" ) as f:   # 打开本地文件
                    f.write("\n\n" + name + ":说")
                    f.write("\n\n" + content)
                    f.close()
                i += 1
            except urllib.error.URLError as e:
                if hasattr(e, "code"):
                    print(e.code)
                if hasattr(e, "reason"):
                    print(e.reason)
                time.sleep(5)
            except Exception as e:
                print("Exception:%s" % str(e))
                time.sleep(1)

#    def write_files(self, data):
#        try:
#            with open("D:/Agan/spider/qiubai/qiubai.txt", "a", encoding="gbk", errors= "ignore" ) as self.open:   # 打开本地文件
#                self.open.write("\n\n" + data[0] + ":说")
#                self.open.write("\n\n" + data[1])
#        except Exception as e:
#            print("Exception:%s" % str(e))
#            
#    def close_file(self):
#        try:
#            self.open.close()
#        except Exception as e:
#            print("Exception: %s" % e)

        
class conurl(threading.Thread):
    def __init__(self, urlqueue):
        threading.Thread.__init__(self)
        self.urlqueue = urlqueue
    def run(self):
        while(True):
            print("程序执行中")
            time.sleep(60)
            if (self.urlqueue.empty()):
                print("程序执行完毕!")
                exit()
                

# proxy = '49.81.254.120:8118'
pagestart = 1
pageend = 10
# 创建线程1，随即启动线程1
t1 = geturl(pagestart, pageend, urlqueue)
t1.start()

# 创建线程2，随即启动线程2
t2 = getcontent(urlqueue)
t2.start()

# 创建线程3，随即启动线程3
t3 = conurl(urlqueue)      
t3.start()

        
```

PS: 本来想用代理Ip爬取的，奈何网上试了好多代理ip都被封掉了，只能取消代理ip进行尝试了（有些注释掉的代码是用来使用代理ip的）

过程如下：
```
第7i16j次入队
第7i17j次入队
第7i18j次入队
第7i19j次入队
第7i20j次入队
第7i21j次入队
第7i22j次入队
第7i23j次入队
第7i24j次入队
第77个网页处理
第78个网页处理
第79个网页处理
第80个网页处理
Exception:list index out of range
第81个网页处理
第82个网页处理
第83个网页处理
第84个网页处理
第8i0j次入队
第8i1j次入队
第8i2j次入队
第8i3j次入队
第8i4j次入队
……
```

结果like

```


篮子里的小猫咪:说

说个真人真事，我老家在农村，八岁的时候我妈生了我妹妹，我爸在外地打工，就我妈一人在家带我和我妹妹，有一天我妈出去干农活了，留我妹妹一人在家睡觉，我放学回去老远就听到我妹妹在哭，把她抱出来放竹篓里，还是哭，我以为她饿了，给她冲了奶粉也不喝，当时赶作业就没管她，过了会儿一股屎臭味悠悠的从竹篓飘了出来，我才知道她是要拉粑粑，然后就把她爆出来准备给她换裤子，当时我人也小，裤子脱不下来，脑壳突然灵光一现，直接把她放院坝里，双手拖着她的裤腿，就在院坝里跑，我妹妹也不哭了，就盯着我嘿嘿嘿的傻笑，之后，裤子给她脱掉了，院坝里到处都是黄灿灿的粑粑，屎味儿也布满了整个院子[流鼻血][流鼻血][流鼻血]

飞沙，风中转:说

小姨子比媳妇小几岁，长的瘦小顶着张娃娃脸，媳妇一直叫她丫头。有天我就说媳妇：她都结了婚的人，你还叫她丫头跟叫小孩子似的。媳妇斜了我一眼，说：我这是时刻提醒你，对小孩子有想法会死的很惨！！！我特么……

高冷☆棒棒:说

开会中，张总讲话：个别同志不知道怎么回事，上班期间哈欠连天，就像没睡醒似的……他话没说完，我忍不住张大嘴巴，打了一个哈欠。周围坐着的人都被我传染了，都张大嘴巴打着哈欠。张总无奈的看着我们，他也打了一个……
……
```
