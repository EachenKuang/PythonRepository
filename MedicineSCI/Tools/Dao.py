# -*- coding: utf-8 -*-

import pymssql


class Dao:
    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self):
        # 数据库连接信息
        self.conn = pymssql.connect(host="localhost:59318", user="eachen", password="123456", database="mydata",
                                    charset="utf8")
        # host = "localhost:59318", user = "eachen", pwd = "123456", db = "mydata"
        self.cur = self.conn.cursor()
        if not self.cur:
            raise (NameError, "数据库连接失败")
        else:
            print("数据库连接成功")

    def create(self, sql):
        # print(sql)
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except:
            print('create failed')
        else:
            print('create succeed')

    def insert(self, sql):
        # print(sql)
        self.cur.execute(sql)
        self.conn.commit()

    def select(self, sql):
        # print(sql)
        self.cur.execute(sql)
        # fetchall()是接收全部的返回结果行
        return self.cur.fetchall()

    def close(self):
        self.conn.close()
