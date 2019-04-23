# -*- coding: utf-8 -*-
"""
@author: Alvin Gan
"""
import pymysql

class mysql(object):
    def __init__(self):  # 初始化连接mysql
        self.__connect__()
        
    def __connect__(self):  # 连接mysql
        try:
            self.conn = pymysql.connect(host = 'localhost',
                                        user = 'root',
                                        passwd = '****',
                                        port = 3306,
                                        db = 'test1',
                                        charset = 'utf8'
                                        )
        except pymysql.Error as e:
            print("Error:%s" % str(e))
            
    def close_conn(self):  # 关闭连接
        try:
            self.conn.commit()
            self.conn.close()
        except pymysql.Error as e:
            print("Error:%s" % str(e))
            
    def execute_sql(self, sql):   # 执行sql,适合插入，修改，删除操作
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.close

    def get_data(self, sql):   # 适合查询数据
        cursor = self.conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        cursor.close()
        
def main(sql):
    t = mysql()
    t.__connect__()
    t.execute_sql(sql)
    t.close_conn()
    
if __name__ == '__main__':
    sql = r'''delete from stu where class_name in ('七班','五班','十八班');'''
    main(sql)
    print('Done')
