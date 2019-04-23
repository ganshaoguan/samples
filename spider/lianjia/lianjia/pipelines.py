# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class LianjiaPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host = 'localhost', user = 'root', passwd = 'agan', db = 'alvin', port = 3306, charset = 'utf8')
        for i in range(0, len(item['title'])):
            title = item['title'][i]
            link = item['link'][i]
            price = item['price'][i]
            unit = item['unit'][i]
            square = item['square'][i]
            house_type = item['house_type'][i]
            height = item['height'][i]
            orientation = item['orientation'][i]
            location = item['location'][i]
            business_region = item['business_region'][i]
            village = item['village'][i]
            traffic = item['traffic'][i]
            longitude = item['longitude'][i]
            latitude = item['latitude'][i]
            sql = '''insert into lianjia(link, title, price, unit, square, house_type, height, orientation, location,
                        business_region,village,traffic,longitude, latitude) values ('%s','%s','%s','%s','%s','%s','%s','%s',
                        '%s','%s','%s','%s', %.6f, %.6f);''' % (title,link, price, unit,square, house_type, height, orientation, location,
                        business_region,village,traffic,longitude, latitude)
            try:
                conn.query(sql)
                conn.commit()
            except pymysql.Error as e:
                print("Error:%s" % str(e))
        conn.close()
        return item
