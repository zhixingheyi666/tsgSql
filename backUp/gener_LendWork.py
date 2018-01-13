# -*- coding: utf-8 -*-
"""
-->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
--生成2016.9至2017.2（上半学年）的借阅记录
--每行开头有四个注释符号，如“----”的，为废弃语句
--同一时间段内，为防止同一本书同时被不同的人借阅，全部读者对应的bid不应重复
--对每个年级分别生成，以一年级为例
--对于法定节假日以及其他工作日的调整，尤其异常调整，如大雪天停课，平时应当记录
--生成日期时，用holiday数组传入

--选取一年级曾经借过的书
--select * from abklendwork a where left(a.loperator,1) = '一';
--select distinct bid from abklendwork a where left(a.loperator,1) = '一';
--选取当前时间一年级读者   		下面语句的基础是部门名称第一个字符是年级 如 ‘一年级3班2022’
--select rid, depname from reader r, department d where left(d.depname,1) = '一' and r.depid = d.depid; 
--select rid from reader r, department d where left(d.depname,1) = '一' and r.depid = d.depid;
--生成临时表，读者写入4次，代表借阅4次
--select rid into AtttRid  from reader r, department d where left(d.depname,1) = '一' and r.depid = d.depid;
--insert into AtttRid select rid from reader r, department d where left(d.depname,1) = '一' and r.depid = d.depid;
--insert into AtttRid select rid from reader r, department d where left(d.depname,1) = '一' and r.depid = d.depid;
--insert into AtttRid select rid from reader r, department d where left(d.depname,1) = '一' and r.depid = d.depid;
--select * from AtttRid;
--drop table Atttrid;
--随机选择bid写入临时表
--select distinct  bid , newid() randUid into AtttBid from abklendwork a where left(a.loperator,1) = '一' order by newid();
--drop table Atttbid;
--select * from Atttbid;
--测试合并两个表





----rid和bid的笛卡尔积
----select a.bid, r.rid from abklendwork a, reader r, department d where left(a.loperator,1) = '一' and left(d.depname,1) = '一' and r.depid = d.depid;
----选取当前时间一年级读者 2016 + 7 - 1 = 2022 ,下面语句的基础是部门名称后四位是用阿拉伯数字表示的学生的毕业年份
----选取某年级读者公式： 当前学年开始年份 + 7 - 在读年级 = 毕业年份
----或者获取dename，用python查找子字符串，匹配‘一年级’
----select rid, depname from reader r, department d where right(d.depname, 4) = right(str((2016 + 7 - 1)),4) and r.depid = d.depid;
----select  len(str((2016 + 7 - 1));--这个字符串的长度是 10 
----select  str(2022);


-->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

"""


#from fc.conn_SQL import mkcon

import random ,pdb

from itertools import zip_longest as myzip 
from fc.conn_SQL import * 
from fc.LOG_sf import logger

cursor, mkconn = mkcon('mic')
#--同一时间段内，为防止同一本书同时被不同的人借阅，全部读者对应的bid不应重复,已经用过的bid放入集合bidInuse

def Bid(grade):
    #bStat函数状态标志，以后每个函数都应包含名为Stat的函数状态标志
    #--选取grade年级曾经借过的书
    global bidInuse
    sql = 'select distinct bid, bcid from abklendwork a where left(a.loperator,1) = \'' + grade + '\''
    cursor.execute( sql )
    rows = cursor.fetchall()
    tSet = set()
    lBid = []
    for row in rows:
        tSet.add( row[0] )
        lBid.append( list(row))
    tSet = tSet - bidInuse
    bidInuse = bidInuse | tSet
    return lBid 

def Rid(grade):
    #rStat函数状态标志，以后每个函数都应包含名为Stat的函数状态标志
    #--选取当前时间grade年级读者   		下面语句的基础是部门名称第一个字符是年级 如 ‘一年级3班2022’
    sql = 'select rid from reader r, department d where left(d.depname,1) = \'' + grade + '\' and r.depid = d.depid' 
    cursor.execute( sql )
    rows = cursor.fetchall()
    tSet = set()
    for row in rows:
        tSet.add(row[0])
    return list( tSet ) 
def lDay( beginDate, endDate, Holiday, Workday, tmp ):
    """
        #先写一个生成整个学期借阅记录日期池的代码 
        #本程序适应的情况：半学年半学年的生成记录
        #beginDate 日期池开始时间 endDate 日期池结束时间 采用的是'yyyy-mm-dd'格式的字符串
        #holiday 起始时间范围内的法定假期，或者其他异常导致的非工作日 workday 起始时间内因调休导致的工作日  
        #   以上连个变量都是list，列表中的每项采用的是'mm-dd'格式的字符
        #ldStat函数状态标志，以后每个函数都应包含名为Stat的函数状态标志
        #--if(beginDate,endDate格式错误)，ldStat=[5,'格式错误']
        #本程序是以Abklendwork中五年的日期为蓝本，生成的借阅日期，用那几年为蓝本，也可以设计成传参数控制。
        #--@ny，借阅记录生成时的年份，@hisy，将要选取的原记录的年份   
        #--@begindate，需要生成记录的起始时间，一般为学期的开始， @enddate，需要生成记录的结束时间，一般为学期的结束   
        #--tt--貌似declare语句声明的变量如@wk,在后面的语句如set语句和后面用到这个变量的语句中无法使用，会返回42000
        #   错误，如果我把他们放在一个execute中执行，才有效。看看是否跟begin 和end有关。
        #2016-2017上半学年
        #2016-09-01   2011-01-14
        #holiday
        #09-15 09-16 09-17 10-01 10-02 10-03 10-04 10-05 10-06 10-07 12-31 01-01 01-02
        #workday
        #09-18 10-08 10-09
        #
        #
        #日期筛选规则:
        #       先筛选bakcdate为周末或者在holiday数组中的记录，将其删除
        #       筛选lenddate为周末且不在workday中，将其日期加入数组holiday，然后为workday生成记录，然后删除holiday记录
        #workday补：
        #       workday记录只从lenddate在workday之后的记录中转移（原则不超过30天）
        #       workday记录优先从有记录的holiday中转移，至少要有一天的记录，
        #       如果不存在符合条件且有记录的holiday，则workday从lendate在workday之后的记录最多的三天中每天转移三分之一
        """
    ny = beginDate[:4] 
    cursor.execute('select distinct year(lenddate) hisy from Abklendwork order by hisy')
    hisys = cursor.fetchall()
    hisy = []
    #清空临时表
    cursor.execute('truncate table AttLendWork')
    for hi in hisys:
        hisy.append( hi[0] )
    for hi in hisy:
        if hi < int(ny):
            #cursor.execute('set @hisy =' + str(hi))  
            #cursor.execute('set @wk = datediff(wk, @hisy, @ny)*7') 
            cursor.execute('select datediff(wk, ?, ?)*7', str(hi), ny) 
            wk = cursor.fetchall()[0][0]
            logger.info(wk)
            #pdb.set_trace()
            #进行下面语句之前，数据库中已经建好一个临时数据表AttLendWork
            sql = """insert into AttLendWork(lenddate, backdate, returndate) \
                    select lenddate + ?, backdate + ?, returndate + ? from abklendwork\
                    where lenddate + ? > ? and backdate + ? < ?;\
                    insert into attlendwork(lenddate, backdate, returndate) \
                    select lenddate + ?-7, backdate + ?-7, returndate + ?-7 from abklendwork\
                    where lenddate + ?-7 > ? and backdate + ?-7 < ?;"""
            cursor.execute( sql, wk,wk,wk, wk,beginDate, wk,endDate, wk,wk,wk, wk,beginDate, wk,endDate)
    #日期筛选整理
    holiday = []
    workday = []
    #yHalf:1，下半学年，0，上半学年，_，未设置
    yHalf = '_' 
    for hi in Holiday:
        #如果开学日期为下半年的日期，跨过元旦，年份应该加一年。
        #这里突出了日期检查的重要，‘2016-09-02’能够正常工作，其他的诸如‘2016-9-2’，‘09-02-2016’都将不能正常运行，月份格式必须为‘09-02’
        if int(beginDate[5:7]) > 7 and (hi[:2] in [ '01','02' ]):
            holiday.append(str(int(ny)+1) + '-' + hi)
            yHalf = '1' 
        else:
            holiday.append(str(int(ny)) + '-' + hi)
            yHalf = '0' 
    for wi in Workday :
        if int(beginDate[5:7]) > 7 and (wi[:2] in [ '01','02' ]):
            workday.append(str(int(ny)+1) + '-' + wi)
        else:
            workday.append(str(int(ny)) + '-' + wi)
    #先筛选bakcdate为周末或者在holiday数组中的记录，将其删除
    sql ='delete from  AttLendWork where datepart(dw, backdate) in (1,7)'
    cursor.execute(sql)
    rowCount = cursor.rowcount
    for hi in holiday:
        sql ='delete from  AttLendWork where CONVERT(varchar(100), backdate, 23) = ?'
        cursor.execute(sql, hi)
        logger.info(rowCount)
        rowCount = rowCount + cursor.rowcount
    tt = 'Delete backdate Effect rows:' + str(rowCount)
    logger.info(tt)
    #筛选lenddate为周末且不在workday中，将其日期加入数组holiday
    sql = 'select distinct CONVERT(varchar(100), lenddate, 23) from  AttLendWork where datepart(dw, lenddate) in (1,7)'
    cursor.execute(sql)
    for li in cursor:
        if li[0] not in workday and li[0] not in holiday:
            holiday.append(li[0])        
    logger.info( holiday )
    #为workday生成记录，然后删除holiday记录
    for wi in workday:
        t = 0
        wcnt = 0
        for hi in holiday:
            cursor.execute('select datediff(dd,?,?)',wi,hi)
            diff = cursor.fetchone()[0]
            if diff < 30 and diff > 0:
                #执行日期替换 
                sql = 'update AttLendWork set lenddate = ? where CONVERT(varchar(100),lenddate,23) = ?'
                cursor.execute(sql, wi, hi)
                wcnt = wcnt + cursor.rowcount
                logger.debug('本次替换:')
                logger.debug(wcnt)
                holiday.remove(hi)
                if wcnt > 0:
                    t = 1
            if wcnt > 30:
                logger.debug("替换超过30条，即可结束替换")
                logger.debug(wcnt)
                break 
        if t == 1: 
            cursor.commit()
        if t == 0:
            try:
                logger.debug("holiday中不存在合格的替换日期，从普通日期中替换")
                #sql = 'update AttLendWork set lenddate = ? where did in (select top 30 did from AttLendWork where lenddate = (select top 1 lenddate from AttLendWork where lenddate > ? group by lenddate order by count(lenddate) desc ))'
                #pdb.set_trace()
                sql = 'select top 1 CONVERT( varchar(100), lenddate, 23) from AttLendWork where lenddate > ? group by lenddate order by count(lenddate) desc'
                cursor.execute(sql,wi)
                tli = cursor.fetchone()[0]
                sql = 'update AttLendWork set lenddate = ? where did in (select top 30 did from AttLendWork where lenddate = ?)'
                cursor.execute(sql,wi,tli)
                logger.debug('本次替换:')
                wcnt = cursor.rowcount
                logger.debug(wcnt)
                if wcnt > 0:
                    cursor.commit()
            except:
                logger.warn('日期 %s 没有合适的替换日期 ' % wi)
    logger.debug('删除lenddate在holiday中的记录')
    sql = 'delete from AttLendWork where CONVERT(varchar(100), lenddate, 23) = ?'
    for hi in holiday:
        cursor.execute(sql,hi)
        logger.debug(cursor.rowcount)
    cursor.commit()
    if tmp:
        toperator = '王' + '_00' 
    else:
        toperator = '王' + ny[2:4] + yHalf
    #pdb.set_trace()
    cursor.execute('update AttLendWork set loperator = ?, boperator = ? where 1=1', toperator, toperator)
    logger.debug(cursor.rowcount)
    cursor.commit()
    logger.info(hisy)
    #return(hisy)
    #for hi in hisy:

        
#随机匹配bid和rid，先使得bid的数目超过bid，然后打乱数组顺序，选取与bid相同数目的rid与bid组成匹配借阅条目
def gener( beginDate, endDate, Holiday, Workday, yearBefore,times = 4, Reader = 'All', tmp = False ):
    #gStat函数状态标志，以后每个函数都应包含名为Stat的函数状态标志
    #times: 本时间段内，平均每生的借阅次数
    #yearBefore:如果生成本学年的，值为0，如果生成上个学年的借阅记录，值为1，上上个学年，值为2，依次类推
    #   如果生成从前年份的借阅记录，比如一年以前，那么现在的六年级就是当时的五年级，对应的bid应当选五年级读者借过的
    #   而原先的六年级已经毕业，所以不用生成了
    if yearBefore > 5 or yearBefore < 0 or type(yearBefore) is not int: 
        gStat = [ 'yearBefore:如果生成本学年的，值为0，如果生成上个学年的借阅记录，值为1，上上个学年，值为2，依次类推', 'yearBefore参数错误', False]
        logger.warn(gStat)
        pdb.set_trace()
        return gStat
    tGrade = [ ['一',2.5], ['二',3.5], ['三',4], ['四',4.5], ['五',5.5], ['六',4] ]
    if yearBefore == 0:
        tGrid = tGbid = tGrade
    else:
        tGrid = tGrade[ yearBefore: ]
        tGbid = tGrade[ : -yearBefore ]
    ttRidBid = []
    trid_num = 0
    for tgr, tgb in myzip( tGrid, tGbid ):
        #pdb.set_trace()
        rid = Rid(tgr[0])
        rL = len(rid)
        trid_num = trid_num + rL
        bid = Bid(tgb[0])
        bL = len(bid)
                #for tg in tGrade:
                #    rid = Rid(tg[0])
                #    rL = len(rid)
                #    trid_num = trid_num + rL
                #    bid = Bid(tg[0])
                #    bL = len(bid)
        #这里如果从前曾经借过的书越多，这个年级生成的条目占比就越多，如此循环，最后可致比例失衡，下面加入比例控制因子
        #一年级生均2.5，二年级3.5，三4，四4.5，五5.5，六4
        #总记录数 = 一年级人数 * 2.5 + 二年级人数 * 3.5 +三年级人数 * 4 +四年级人数 * 4.5 +五年级人数 * 5.5 +六年级人数 * 4
        if( bL <= rL ):
            return False 
        rid = rid * ( bL//rL + 1 ) 
        random.shuffle(rid) 
        random.shuffle(bid) 
        rid = rid[:bL]
        if bL > rL * tgb[1]:
            bL = round(rL * tgb[1])
        for i in range(bL):
            ti = bid[i] + [rid[i]]
            ttRidBid.append(ti)
    #pdb.set_trace()
    random.shuffle(ttRidBid) 
    logger.debug('生成日期条目:')
    lDay( beginDate, endDate, Holiday, Workday, tmp )
    #读者、日期匹配规则：
    #       先把所有lenddate出现次数少于50的记录全匹配一遍（避免日期丢失问题），然后剩余读者的按概率随机匹配
    try:
        sql = 'select count(lenddate) cn,CONVERT(varchar(100), lenddate, 23) lenddate into #t1 from AttLendWork group by lenddate'
        cursor.execute(sql)
    except:
        cursor.execute('truncate table #t1')
        sql = 'insert into #t1 select count(lenddate) cn,CONVERT(varchar(100), lenddate, 23) lenddate from AttLendWork group by lenddate'
        cursor.execute(sql)
    sql = 'select did from AttLendWork where CONVERT(varchar(100), lenddate, 23) in (select lenddate from #t1 where cn < 50)' 
    cursor.execute(sql)
    Adid = set() 
    for ci in cursor.fetchall():
        Adid.add(ci[0])
    tnum = len(ttRidBid) - len(Adid)
    if tnum > 0:
        #--从剩余的日期条目随机抽取匹配读者条目,先抽取3倍需要量，再截取
        #pdb.set_trace()
        sql = 'select top %s did from AttLendWork order by checksum(newid())' % (str(tnum*3)) 
        cursor.execute(sql)
        Bdid = set() 
        for ci in cursor.fetchall():
            Bdid.add(ci[0])
        Cdid = list(Bdid - Adid)
        random.shuffle(Cdid) 
        #汇聚所有用于生成记录的日期条目
        Ddid = Cdid[:tnum] + list(Adid)
    else:
        Ddid = list(Adid)
    Ddid.sort()
    tLendWork = []
    for i in range(len(ttRidBid)):
        ttRidBid[i].append(Ddid[i])
        tLendWork.append(tuple(ttRidBid[i]))
    #pdb.set_trace()
    logger.info('预备有 %s 条记录写入LendWork' % len(tLendWork))
    sql = 'insert into LendWork( bid, Bcid, Rid, LendDate, ReturnDate, BackDate, loperator, boperator ) select ?, ?, ?, LendDate, ReturnDate, BackDate, loperator, boperator from AttLendWork where did = ?' 
    cursor.executemany(sql, tLendWork)
    #for i in tLendWork:
    #    cursor.execute(sql, i)
    #    cursor.commit()
    #logger.info(cursor.rowcount)
    cursor.commit()
    #pdb.set_trace()
    logger.info('Success!')
if __name__ == '__main__':
    o1 = 2
    o2 = 2
    if o1>1:
         bidInuse = set()
         beginDate = '2017-02-14'
         endDate = '2017-06-11'
         holiday = [  '04-02','04-03','04-04','04-29','04-30','05-01','05-28','05-29','05-30']
         workday = ['04-01','05-27']
         gener( beginDate, endDate, holiday, workday, yearBefore = 0, tmp = 1 )
    if o1>1:
         bidInuse = set()
         beginDate = '2016-09-02'
         endDate = '2017-01-12'
         holiday = [ '09-15', '09-16', '09-17', '10-01', '10-02', '10-03', '10-04', '10-05', '10-06', '10-07', '12-31', '01-01', '01-02' ]
         workday = ['09-18', '10-08', '10-09']
         gener( beginDate, endDate, holiday, workday, yearBefore = 0 )
    if o1>1:
         bidInuse = set()
         beginDate = '2016-02-25'
         endDate = '2016-07-05'
         holiday = [  '04-02','04-03','04-04','04-30','05-01','05-02','06-09','06-10','06-11']
         workday = ['06-12']
         gener( beginDate, endDate, holiday, workday, yearBefore = 1, tmp = 0 )
    if o1>1:
         bidInuse = set()
         beginDate = '2015-09-01'
         endDate = '2016-01-25'
         holiday = [ '09-03', '09-04', '09-05', '09-26', '09-27', '10-01', '10-02', '10-03', '10-04', '10-05', '10-06', '10-07', '01-01', '01-02', '01-03' ]
         workday = ['09-06', '10-10']
         gener( beginDate, endDate, holiday, workday, yearBefore = 1, tmp = 0 )
    if o1>1:
         bidInuse = set()
         beginDate = '2015-03-09'
         endDate = '2015-07-03'
         holiday = [  '04-04','04-05','04-06','05-01','05-02','05-03','06-20','06-21','06-22']
         workday = []
         gener( beginDate, endDate, holiday, workday, yearBefore = 2, tmp = 0 )
    if o1>1:
         bidInuse = set()
         beginDate = '2014-09-01'
         endDate = '2015-02-05'
         holiday = [ '09-05', '09-06', '09-07', '09-26', '09-27', '10-01', '10-02', '10-03', '10-04', '10-05', '10-06', '10-07', '01-01', '01-02', '01-03' ]
         workday = ['09-28', '10-11', '01-04']
         gener( beginDate, endDate, holiday, workday, yearBefore = 2, tmp = 0 )
    if o1>1:
         bidInuse = set()
         beginDate = '2014-02-17'
         endDate = '2014-07-03'
         holiday = ['04-05','04-06','04-07','05-01','05-02','05-03','05-31','06-01','06-02']
         workday = ['05-04']
         gener( beginDate, endDate, holiday, workday, yearBefore = 3, tmp = 0 )
    if o1>1:
         bidInuse = set()
         beginDate = '2013-09-02'
         endDate = '2014-01-15'
         holiday = ['09-19','09-20', '09-21', '10-01', '10-02', '10-03', '10-04', '10-05', '10-06', '10-07', '01-01']
         workday = ['09-22', '09-29', '10-12']
         gener( beginDate, endDate, holiday, workday, yearBefore = 3, tmp = 0 )
    if o1>1:
         bidInuse = set()
         beginDate = '2013-02-18'
         endDate = '2013-07-04'
         holiday = [ '04-04','04-05','04-29','04-30','05-01','06-10','06-11','06-12']
         workday = ['04-07','04-27','04-28','06-08','06-09']
         gener( beginDate, endDate, holiday, workday, yearBefore = 4, tmp = 0 )
    if o1>1:
         bidInuse = set()
         beginDate = '2012-09-03'
         endDate = '2013-01-15'
         holiday = [ '09-30', '10-01', '10-02', '10-03', '10-04', '10-05', '10-06', '10-07', '01-01', '01-02', '01-03' ]
         workday = ['09-29', '10-08', '01-05', '01-06']
         gener( beginDate, endDate, holiday, workday, yearBefore = 4, tmp = 0 )
    #测试用句>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #测试用句>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #测试用句>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #测试用句>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #hisy = lDay( beginDate, endDate, holiday, workday )
    #Lw = gener('2015')
    #rows = Bid( '一' )
    #rid = Rid( '一' )
