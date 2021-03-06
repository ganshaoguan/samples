### 目标：爬取糗事百科文字部分，包括用户名 + 内容
### 链接：https://www.qiushibaike.com/text/
### 分析网页发现 
1. 有些内容由于过长并未完全显示在主页面内，需要打开文章对应的链接才能完全爬取到文字内容；
2. 主页分页链接如下 ：https://www.qiushibaike.com/text/page/2/  ，page后面的参数表示页码；


### 总结，需要三步走，1 .生成分页链接，2 .爬取分页链接里的文章链接， 3.爬取文章链接里的内容


```python
# -*- coding:utf-8 -*-
__author__ = 'Alvin Gan'


import re
import urllib.request
import urllib.error

# 添加报头
headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36')
opener = urllib.request.build_opener()
opener.addheaders = [headers]
urllib.request.install_opener(opener)


# 爬取分页url， 因为有的页面需要查看全文
def url_list(url, page):
    link = url + str(page) + "/"            # 构建url
    data1 = urllib.request.urlopen(link).read().decode('utf-8')
    data = str(data1)
    pat = r'''<a href="(.*?)" target="_blank" class="contentHerf" onclick="_hmt.push'''   # 每篇文章的id
    result = re.compile(pat).findall(data)
    return result       # 返回一个列表值，like ["/article/119521405", "/article/11952140"]


# 爬取作者和正文
def craw(url, result):
    link = url + result         # 构建每篇文章的url
    data1 = urllib.request.urlopen(link).read().decode('utf-8')
    data = str(data1)
    name_pat = r'''<a href="/users/\w*?/" target="_blank" title=".*?">
<h2>(.*?)</h2>'''
    content_pat = r'''<div class="content">

(.*?)

</div>'''

    name = re.search(name_pat, data).group(1) + " ：说"
    content = re.search(content_pat, data).group(1)
    content.strip()
    content = content.replace("<br/>", "")
    return name,content     # 返回一个set, name 和 content分别表示作者和内容


def write_files(s):   # 写入本地文本文件
    with open("D:/Agan/spider/qiubai/qiubai.txt", "a", encoding="gbk", errors= "ignore" ) as f:
        for file in s:
            f.write("\n\n" + file)
        f.close()
        
        
# 执行
        
if __name__ == "__main__":
    try:
        for page in range(1, 31):
            url1 = "https://www.qiushibaike.com/text/page/"
            article_url_list = url_list(url1, page)
            print("正在爬取第%d页" % page)
            for article_url in article_url_list:
                url2 = "https://www.qiushibaike.com"
                try:
                    s = craw(url2, article_url)
                except AttributeError as e:   # 后验证发现有些用户为匿名用户，re提取name时会报错，将这些匿名用户忽略掉
                    print(e)
                    print(url2 + article_url)
                    continue
                num = article_url_list.index(article_url) + 1
                print("正在爬取本页第%d位用户" % num)
                write_files(s)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    print("已完成")
    
```

在测试过程中由于运行次数太多，被网站暂时封了ip， 看来还是需要用代理ip地址啊,代理ip目前还没学，日后再说

运行过程如下：

```python

正在爬取第1页
正在爬取本页第1位用户
正在爬取本页第2位用户
正在爬取本页第3位用户
正在爬取本页第4位用户
'NoneType' object has no attribute 'group'      # 报错表示为匿名用户
https://www.qiushibaike.com/article/104915816
正在爬取本页第6位用户
正在爬取本页第7位用户
正在爬取本页第8位用户
正在爬取本页第9位用户

……

```


爬取结果如下：

```python

你就是个刽子手 ：说

哥嫂生了两小孩，现在小的都6岁了，一直说很久没过二人世界了，这是背景…………………割……………………昨天上午，哥打电话来说，要和嫂子出去一趟，家里没人做饭，叫我们照顾两小孩一天，两小孩中饭晚餐都是在我家吃的，晚上八点多，由于小孩没带换洗衣服，我只好去哥家帮小孩拿衣服，我打开门的那一瞬间，居然看到哥嫂两人正抱在一起跳舞，旁边居然红酒，牛排，蜡烛，音乐齐全，敢情两人在烛光晚餐，太投入了没听到我的开门声，你们……干得漂亮，就是牛排不是我喜欢的全熟

我就聊聊不泡你 ：说

周末回家，老妈去外婆家了，我和老爸在家，刚好晚上停电，我们只好在柴火灶上煮饭吃。吃着吃着，突然看到老爸眼角闪着泪花，忙问老爸咋了。老爸擦擦眼泪：“那时候你还小，家里还没通电，每天干活回来，我烧火，你妈做饭……”我连忙安慰：“没事的老爸，苦日子都过去了。”老爸一脸茫然：“什么苦日子？我是说这柴火饭的锅巴还是那么噎人，老子眼泪都噎出来了！”

哇塞～小仙女 ：说

老公送我回娘家。。。在家门口老公摩托车压到只鸭子…当时没在意，鸭子瘸了条腿！老公来接我回家，又压了那只瘸鸭子…吃饭的时候多了个肉菜！！老爸心疼的看着鸭子说：没事别回来了，糟蹋鸭子。。

……

```



但是，在运行代码片段，如果仔细观察会发现，每次循环都会调用 write_files() 函数，而该函数每次都执行都会运行 “打开文件-写入内容-关闭文件” 的操作，如果只打开一次文件，将全部内容写入后再关闭文件应该会缩短爬取时间


```python
if __name__ == "__main__":
    try:
        with open("D:/Agan/spider/qiubai/qiubai.txt", "a", encoding="gbk", errors= "ignore" ) as f:
            for page in range(1, 4):
                url1 = "https://www.qiushibaike.com/text/page/"
                article_url_list = url_list(url1, page)
                print("正在爬取第%d页" % page)
                for article_url in article_url_list:
                    url2 = "https://www.qiushibaike.com"
                    try:
                        s = craw(url2, article_url)
                    except AttributeError as e:
                        print(e)
                        print(url2 + article_url)
                        continue
                    num = article_url_list.index(article_url) + 1
                    print("正在爬取本页第%d位用户" % num)
                    f.write("\n\n" + s[0])
                    f.write("\n\n" + s[1])
            f.close()
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    print("已完成")
    
```
酱紫就弃用了 write_files()函数，爬取速度会快一些
