在爬取信息的过程中经常会遇到一些网站对ip地址有限制，频繁访问会被禁ip，这时需要使用代理ip地址进行访问，下面爬取一下代理ip

```python

# -*- coding:utf-8 -*-
__author__ ="Alvin Gan"

import requests
from bs4 import BeautifulSoup
import random   # 随机提取一个ip使用

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}

# 爬取代理ip，从xici 上爬取
# url = http://www.xicidaili.com/nn/1  , 尾数 1 是page参数，翻页时修改page参数即可



def ip_list(ip_url, headers, page = 5): # 默认爬取5页
    ip_list = []
    for i in range(1, page + 1):
        url = ip_url + str(i)
        req = requests.get(url, headers = headers)
        req.encoding = 'utf-8'
        soup = BeautifulSoup(req.text, "lxml")
        ips = soup.find_all("tr")
        for i in range(1, len(ips)):    # 这部分需要根据页面来理解
            ip_info = ips[i]
            td_info = ip_info.find_all("td")
            ip_list.append(td_info[1].text + ":" + td_info[2].text)
    return ip_list


# 由于有些代理ip是无效的，需要进行判别，将无效的ip地址删除掉
def usefull_ip(ip_list):   # 提取有效ip
    usefull_ip = []
    for ip in ip_list:
        try:
            requests.get("https://www.baidu.com/", proxies={"http":ip})
            # 这里以访问百度来进行判别
        except:
            continue
        else:
            usefull_ip.append(ip)
    return usefull_ip

def random_ip(ips):  # 随机抽取ip   # random 随机抽取一个ip地址使用
    proxy_list = []
    for ip in ips:
        proxy_list.append("http://" + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {"http": proxy_ip}
    return proxies

ip_url = "http://www.xicidaili.com/nn/"
ips = ip_list(ip_url, headers)
use_ip = usefull_ip(ips)
proxies = random_ip(use_ip)  # 提取随机ip地址
print(proxies)



```
