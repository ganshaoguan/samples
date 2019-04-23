# -*- coding: utf-8 -*-
"""
Created on Thu May 17 17:14:41 2018
@author: Alvin Gan
"""

'''
目的：爬腾讯新闻“要闻” 和 “娱乐" tab 下的新闻标题，只爬取首页
'''


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import datetime as dt
import pandas as pd

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}

class Crawlnewsname(object):
    # url = 'http://news.qq.com/'
    # headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    def __init__(self,url):
        self.url = url
        self.res = requests.get(self.url, headers = headers)
        self.soup = BeautifulSoup(self.res.text, 'html.parser')
        
    def major_news(self):
        data = self.soup.select('div[class="item major"]')
        result = []
        for name in data[0].select('a[class="linkto"]'):
            if len(name.text) >0:
                newsdict = {}
                newsdict['name'] = name.text.strip()
                newsdict['link'] = name['href']
                result.append(newsdict)
            else:
                pass
        return result
        
        
    def ent_news(self):
        data = self.soup.select('div[class="item ent"]')
        result = []
        for name in data[0].select('a[class="linkto"]'):
            if len(name.text) >0:
                newsdict = {}
                newsdict['name'] = name.text.strip()
                newsdict['link'] = name['href']
                result.append(newsdict)
            else:
                pass
        return result
    

def to_excel(df, path):
    ctime = datetime.now()
    delta = dt.timedelta(days = 3)  # 日期顺延三日
    next_time = ctime + delta
    result_time = next_time.strftime('%Y-%m-%d')
    df['date'] = result_time  # 添加日期字段
    names = ['date','catagory','name','link']
    df = df.reindex(columns = names)
    df.to_excel(path + '\\' + result_time + '.xlsx', index = False)   # 以日期命名文件
    


if __name__ == '__main__':
    url = 'http://news.qq.com/'
    news = Crawlnewsname(url)  # 创建对象
    major = news.major_news()  # 爬要闻
    ent = news.ent_news()	   # 爬娱乐新闻
    major_df = pd.DataFrame(major)    # 使用pandas整理数据
    major_df['catagory'] = 'major' # 添加固定字段
    ent_df = pd.DataFrame(ent)
    ent_df['catagory'] = 'ent'
    combine_df = pd.concat([major_df, ent_df])
    path = r'D:\日常数据\日常push'
    to_excel(combine_df, path)
