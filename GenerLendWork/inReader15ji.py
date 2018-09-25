# -*- coding: utf-8 -*-
"""
    本程序用于向金典图书管理程序的数据库导入读者数据
        读者的部门需要提前在图书管理程序中建立，并记录下DepID（部门id），Rgid（读者权限id）
        password可以用randrom函数自动生成，idDisp可以用程序生成（部门内部唯一即可），这两项其实可以为NULL
        
        读者Name和Rid则需要事先按行对应存入datasource文本文件
        
    下面是micsql查询时用到的相关语句,去掉双短横线注释即可应用
    --select * from Reader order by Rid desc;
    --select count(*) from Reader;
    --insert into Reader 
    --select rgid from Reader group by rgid;
    --select count(idDisp) as cnt, idDisp from Reader group by idDisp order by iddisp;
    --select * from Reader where rgid = 19;
    --insert into Reader ( Name, Rid, DepID, Rgid) values ( '测试2', '00031', 45, 19);
    --select *, DepID, idDisp from Reader  where DepID = 52 order by Rid;
    --delete from Reader where rid = '000300';
    --select count(distinct DepID) from Reader;
    --select * from department;
    --2015级一、二、三班 DepID 49,50,51	
    --包含idDisp列的表有--->	;BorrowRightList	;skList		;FromList	;jcff	;jcpc	;jcrk	;Reader
    --在Read中，idDisp的规则是从本部门第一个读者开始按照1,2,3...的规律增加guestguest
    
        
"""


import pdb, random, re, random

from fc.conn_SQL import mkcon
from fc.LOG_sf import logger

cursor, miconn = mkcon( s = 'mic' )

def importReader( fname, DepID, Rgid, cursor = cursor, miconn = miconn ):
    logger.info('Func ----> importReader( fname, DepID, Rgid, cursor = cursor, miconn = miconn )')
    fdata = open( fname, 'r' )
    flines = fdata.readlines()
    try:
        cursor.execute( 'select idDisp from Reader where DepID = ? order by idDisp', DepID )
        tidsp = cursor.fetchall()
    except:
        #tidsp = None 
        pass
    if tidsp:
        ti0 = set( range( 1, len(flines) + tidsp[-1][0] + 1 ) )
        ti1 = set()
        for tii in tidsp:
            ti1.add( tii[0] )
        idsp = list( ti0 - ti1 )
        idsp.sort
    else:
        idsp = list( range( 1, len(flines) + 1 ) )
    logger.info(idsp)
    ts = []
    cnt = 0
    for ifl in flines:
        tn = re.split('\t|\n',ifl)
        ttn = tn[:2] + [ DepID, Rgid , idsp[ cnt ], str(random.randint( 100000, 999999 )) ]
        ts.append( tuple(ttn) )
        cnt += 1
    logger.debug(ts)
    cursor.executemany( 'insert into Reader ( Name, Rid, DepID, Rgid, idDisp, GuestPassWord ) values ( ?, ?, ?, ?, ?, ?)', ts )
    miconn.commit()
    
if __name__ == '__main__':
    #fname = 'd:\python_learn\sql\Data\\15test.txt'
    # fname = None
    fname = 'd:\python_learn\sql\Data\\17_1.txt'
    DepID = 61
    Rgid = 19
    importReader(fname,DepID,Rgid)
