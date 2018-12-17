# -*- coding: utf-8 -*-


import random, pdb, datetime
from itertools import zip_longest as myzip

from fc.conn_SQL import *
from fc.LOG_sf import logger

cursor, mkconn = mkcon('mic')

# from RidBidDate import Rid, Bid, lDay

def gener_books( num='',Bcid="I999/9999", Clerk='王_00', State=0, EnterDate='', price=11, sk=2, inForm='', Ddid=None,temp=False, tempNum=0):
    # # 临时指定必要的参数，每次程序运行前，根据需要修改，并反注释
    # # ·考虑将以下参数随机化，以便增加真实性
    # # Bcid必须是Booklist表中存在的，否则会报错
    # Bcid ='I267/234'
    # #··sql数据库中类型为datetime的列，可以用时间字符串的格式插入，例如'2018-10-17 08:26:28.297'
    # EnterDate = '2018-10-17 08:26:28.297'
    # Bid = ['0'+str(i) for i in range(60000, 60000+num)]
    # #相应的总括登记号
    # inForm = 8

    # 生成插入是的数据
    books = [(Bcid, bid, State, Clerk, EnterDate, price, sk, inForm) for bid in Bid]

    # 如果没有指定必须的参数，程序将退出
    if enterDate == '' or inForm == '' or Ddid != None:
        num = ''
    if num == '':
        logger.warn("-------------------程序缺少必要的参数!!------------------\n")
        return

    # Values后面括号了的?必须用逗号分隔，不然报错
    sql = """insert into bookclass(Bcid, Bid, State, Clerk, EnterDate, price, sk, inForm) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.executemany(sql, books)
    # cursor.execute(sql)
    mkconn.commit()
    # sql = "select * from bookclass where Clerk = '王_00'"
    # cursor.execute(sql)
    # for ci in cursor.fetchall():
    #     print(ci)


if __name__ == '__main__':
    gener_books(num=175)
