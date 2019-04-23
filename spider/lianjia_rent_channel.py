# -*- coding:utf-8 -*-
__author__ = 'Alvin Gan'

import requests, pymysql
from bs4 import BeautifulSoup


def getUrl(url):	# 抓取每个房源的url链接，该函数url参数为分页链接
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, "html.parser")
    link = []
    for info in soup.select(".info-panel"):
        if len(info.select("h2"))<=0:
            pass
        else:
            link.append(info.select("h2 a")[0]["href"])		# 提取链接
    return link


def getDetails(detailurl):	# 抓取房源详细信息，存储到result
    summary = {}
    res = requests.get(detailurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, "html.parser")
    title = soup.select(".content .title .main")[0].text     # 标题
    price = soup.select(".price .total")[0].text             # 价格
    unit = soup.select(".price .unit")[0].text.strip()       # 价格单位
    decoration = soup.select(".price span")[-1].text         # 装修
    square = soup.select(".zf-room .lf")[0].text             # 面积
    house_type = soup.select(".zf-room .lf")[1].text         # 户型
    height = soup.select(".zf-room .lf")[2].text             # 楼高
    orientation = soup.select(".zf-room .lf")[3].text        # 朝向
    location = soup.select(".zf-room p")[-2].text            # 位置
    village = soup.select(".zf-room p")[-3].text.split("\n")[0]   # 小区
    traffic = soup.select(".zf-room p")[4].text              # 交通
    comment = soup.select(".content .title .sub")[0].text    # 卖点
    summary["url"] = detailurl
    summary["title"] = title
    summary["price"] = price
    summary["unit"] = unit
    summary["decoration"] = decoration
    summary["square"] = square
    summary["house_type"] = house_type
    summary["height"] = height
    summary["orientation"] = orientation
    summary["location"] = location
    summary["village"] = village
    summary["traffic"] = traffic
    summary["comment"] = comment
    return summary

def import_to_mysql(sql):  # 将数据导入到mysql
    db = pymysql.connect(host = "localhost", user = "root", password = "password", db = "db", charset="utf8") # 请注意此处的数据库密码和数据库的修改
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()




if __name__ == '__main__':
    sumlink = []
    for i in range(1,3):
        url = "https://bj.lianjia.com/zufang/pg{}/".format(i)   # 链家租房网站分页链接是根据pg后的数字来定的
        a = getUrl(url)
        sumlink.extend(a)
    for detailurl in sumlink:
        summary = getDetails(detailurl)
        sql = '''insert into homelink_rent(comment, decoration, height,house_type,location,orientation,price,square,title,traffic,unit,url,village)values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (summary["comment"],summary["decoration"],summary["height"],summary["house_type"],summary["location"],summary["orientation"],summary["price"],summary["square"],summary["title"],summary["traffic"],summary["unit"],summary["url"],summary["village"])
        print("正在导入:", summary["url"],summary["title"])
        import_to_mysql(sql)
    print("已全部导入，任务结束")
