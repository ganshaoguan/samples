#链接本地数据库，查询学生成绩表 test1.stu,并将结果输出到本地，建立定时任务，每天执行一次
# -*- coding: utf-8 -*-

import pandas as pd
import pymysql
import time   # 定时任务每天输出的文件按日期命名

print("Start connect mysql!")

class conn_mysql(object):
    def __init__(self):
        self._connect()  # 初始化连接mysql
        
    def _connect(self):
        try:
            self.conn = pymysql.connect(host = 'localhost',
                                        user = 'root',
                                        passwd = '****',  # 使用自己的密码
                                        db = 'test1',
                                        port = 3306,
                                        charset = 'utf8')
        except pymysql.Error as e:
            print("Error:%s"%str(e))
            
    def close(self):
        self.conn.commit()
        self.conn.close()
        
    def search(self, sql):
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql)
        data = self.cursor.fetchall()  # 返回数据
        self.cursor.close()
        return data

print("Connect Success!")

if __name__ == '__main__':
    sql = r'''select * from stu limit 10;'''
    connect = conn_mysql()  # 创建对象
    data = connect.search(sql)  # 查询，返回数据
    connect.close()  # 关闭连接
    p_date = time.strftime("%Y-%m-%d", time.localtime())  # 获得当前日期，返回 yyyy-mm-dd 格式
    df = pd.DataFrame(list(data), columns = ['id','class_name','stu_id','score'])  # 将数据转化成Dataframe格式
    df.to_excel(r"""C:\Users\dianjoy\Desktop\%s.xlsx""" % p_date, 
                sheet_name = 'stu',
                index = False)   # 输出结果到本地
    print("Congratulations! Everything is done!")  # 任务完成





# df数据格式如下，df.to_excel， index= False舍弃掉索引列


"""
   id calss_name stu_id  score
0   1   classOne   1001     89
1   2   classOne   1002     98
2   3   classOne   1003     59
3   4   classOne   1004     76
4   5   classOne   1005     98
5   6   classTwo   2001     76
6   7   classTwo   2002     89
7   8   classTwo   2003     59
8   9   classTwo   2004     93
9  10   classTwo   2005     88

"""
