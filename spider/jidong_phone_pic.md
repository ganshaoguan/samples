```python

# -*-coding:utf-8 -*-
__author__ = "Alvin GAN"
# 爬取京东手机频道手机照片,用到urllib库和re库

import re
import urllib.request
import urllib.error
# https://list.jd.com/list.html?cat=9987,653,655&page=1
# 经分析得到，手机频道的网址是固定的，翻页需要根据page后面的参数来定

def craw(url, page):    # 此处设置两个参数，一个是url，一个是页数
    html1 = urllib.request.urlopen(url).read()
    html = str(html1)
    pattern = '<img width="220" height="220" data-img="1" data-lazy-img="//(.*?\.jpg)">'
    # 观察得知 图片链接都是以这种格式存在的，需用正则表达式提取图片链接，惰性匹配
    result = re.compile(pattern).findall(html)
    x = 1
    for imageurl in result:
        imagename = "D:/Agan/spider/jd/phone_image/" + str(page) + str(x) + ".jpg"    # 存放路径，若路径不存在会报错
        imageurl = "http://" + imageurl
        try:
            urllib.request.urlretrieve(imageurl, filename = imagename)
            print("已完成第%d页第%d条" % (page, x))
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                x += 1
            if hasattr(e, "reason"):
                x += 1
        x += 1


if __name__ == "__main__":
    for i in range(1, 11):  #爬取前十页手机照片
        url = "https://list.jd.com/list.html?cat=9987,653,655&page=%d" % i
        craw(url, i)
```

执行后如下：
```

已完成第1页第1条
已完成第1页第2条
已完成第1页第3条
已完成第1页第4条
已完成第1页第5条
已完成第1页第6条
已完成第1页第7条
已完成第1页第8条
已完成第1页第9条
已完成第1页第10条
已完成第1页第11条
已完成第1页第12条
……

```

照片如下

![爬取结果照片](https://git.oschina.net/uploads/images/2017/0908/143238_a80c1a44_1367680.jpeg "微信图片_20170908143059_副本.jpg")
