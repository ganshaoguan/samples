# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lianjia.items import LianjiaItem
from scrapy.http import Request
import json
import urllib.request
import time
import random

class RentSpider(CrawlSpider):
    name = 'rent'
    allowed_domains = ['lianjia.com']
    '''
    start_urls = ['http://lianjia.com/']
    '''
    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        # proxy = '127.0.0.1:8888'
        for i in range(2, 62):
            url = 'https://bj.lianjia.com/zufang/pg%s/' % str(i) 
            yield Request(url,headers = headers, meta = {'proxy':'http://127.0.0.1:8888'})  

    rules = (
        Rule(LinkExtractor(allow=r'https://bj.lianjia.com/zufang/[0-9]+?.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = LianjiaItem()
        i['title'] = response.xpath('//h1[@class="main"]/text()').extract()
        
        i['link'] = ['https://bj.lianjia.com/zufang/' + response.xpath('//span[@class="houseNum"]/text()').extract()[0].replace('链家编号：', '') + '.html']
        
        i['price'] = response.xpath('//span[@class="total"]/text()').extract()
        i['unit'] = response.xpath('//span[@class="unit"]//span/text()').extract()
        i['square'] = response.xpath('//div[@class="zf-room"]/p[i[text()="面积："]]/text()').extract()
        i['house_type'] = [response.xpath('//div[@class="zf-room"]/p[i[text()="房屋户型："]]/text()').extract()[0].split(' ')[0]]
        i['height'] = response.xpath('//div[@class="zf-room"]/p[i[text()="楼层："]]/text()').extract()
        i['orientation'] = response.xpath('//div[@class="zf-room"]/p[i[text()="房屋朝向："]]/text()').extract()
        i['location'] = [response.xpath('//div[@class="zf-room"]/p[i[text()="位置："]]/a/text()').extract()[0]]
        i['business_region'] = [response.xpath('//div[@class="zf-room"]/p[i[text()="位置："]]/a/text()').extract()[1]]
        i['village'] = [response.xpath('//div[@class="zf-room"]/p[i[text()="小区："]]/a/text()').extract()[0]]
        i['traffic'] = response.xpath('//div[@class="zf-room"]/p[i[text()="地铁："]]/text()').extract()
        
        # 根据小区名称获取小区的经纬度，通过百度的api接口来进行
        # http://api.map.baidu.com/geocoder?key=f247cdb592eb43ebac6ccd27f796e2d2&address=北京
        api_url = 'http://api.map.baidu.com/geocoder/v2/?output=json&ak=*****使用自己申请的key*****&city=%E5%8C%97%E4%BA%AC%E5%B8%82&address=' + urllib.request.quote(i['village'][0])
        print(api_url)
        data = urllib.request.urlopen(api_url).read().decode('utf-8')
        print(data)
        result = json.loads(data)
        print(result)
        try:
            i['longitude'] = [result['result']['location']['lng']]
            i['latitude'] = [result['result']['location']['lat']]
        except Exception as e:
            print('Error:这个地点没有查到对应的经纬度---- %s' % str(e))
            i['longitude'] = [0]
            i['latitude'] = [0]
        
        a = random.randint(0,5)
        time.sleep(a)
        print("休息%s秒..." % str(a))
        print(i['title'])
        print(i['link'])
        print(i['price'])
        print(i['location'])
        print(i['village'])
        print(i['traffic'])
        print(i['business_region'])
        print(i['longitude'])
        print(i['latitude'])
        print('---------')
        return i