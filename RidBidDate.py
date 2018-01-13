#_*_coding:utf-8_*_

__author__ = 'Master Wang'


from fc.LOG_sf import logger

from fc.conn_SQL import *
cursor, mkconn = mkcon('mic')

bidInuse = set()

# --同一时间段内，为防止同一本书同时被不同的人借阅，全部读者对应的bid不应重复,已经用过的bid放入集合bidInuse

def Bid(grade):
    # bStat函数状态标志，以后每个函数都应包含名为Stat的函数状态标志
    # --选取grade年级曾经借过的书
    # ??缺少把普通的借阅记录转换到abklendwork中去的sql语句和规范,abklendwork怎样产生的？gu
    global bidInuse
    sql = 'SELECT DISTINCT bid, bcid FROM abklendwork a WHERE left(a.loperator,1) = \'' + grade + '\''
    cursor.execute(sql)
    rows = cursor.fetchall()
    tSet = set()
    lBid = []
    for row in rows:
        tSet.add(row[0])
        lBid.append(list(row))
    tSet = tSet - bidInuse
    bidInuse = bidInuse | tSet
    return lBid


def Rid(grade):
    # rStat函数状态标志，以后每个函数都应包含名为Stat的函数状态标志
    # --选取当前时间grade年级读者   		下面语句的基础是部门名称第一个字符是年级 如 ‘一年级3班2022’
    sql = 'SELECT rid FROM reader r, department d WHERE left(d.depname,1) = \'' + grade + '\' AND r.depid = d.depid'
    cursor.execute(sql)
    rows = cursor.fetchall()
    tSet = set()
    for row in rows:
        tSet.add(row[0])
    return list(tSet)


def lDay(beginDate, endDate, Holiday, Workday, tmp, temp=False):
    # temp 是一个bool值，当其为真，表示生成的借阅记录仅仅为了应对学期中间的临时检查
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
    cursor.execute('SELECT DISTINCT year(lenddate) hisy FROM Abklendwork ORDER BY hisy')
    hisys = cursor.fetchall()
    hisy = []
    # 清空临时表
    cursor.execute('TRUNCATE TABLE AttLendWork')
    for hi in hisys:
        hisy.append(hi[0])
    for hi in hisy:
        if hi < int(ny):
            # cursor.execute('set @hisy =' + str(hi))
            # cursor.execute('set @wk = datediff(wk, @hisy, @ny)*7')
            cursor.execute('select datediff(wk, ?, ?)*7', str(hi), ny)
            wk = cursor.fetchall()[0][0]
            logger.info(wk)
            """
            # backdate < endDate 说明本程序没有考虑学期中间有临时检查的来，学期中间可以有未归还的书籍
            # 未归还的书籍backdate应当为NULL,boperator也应当为NULL
            # 上面的要求不难实现，首先更改下面语句的时间选择范围，更改 backdate < endDate 为  lenddate < endDate
            # 最后将生成的日期池中的backdate > endDate 的backdate 置为 NULL ，同时将boperator也置为NULL 
            #pdb.set_trace()
            #进行下面语句之前，数据库中已经建好一个临时数据表AttLendWork
            """
            # temp 是一个bool值，当其为真，表示生成的借阅记录仅仅为了应对学期中间的临时检查
            if not temp:
                sql = """INSERT INTO AttLendWork(lenddate, backdate, returndate) 
                    SELECT lenddate + ?, backdate + ?, returndate + ? FROM abklendwork\
                    WHERE lenddate + ? > ? AND backdate + ? < ?;\
                    INSERT INTO attlendwork(lenddate, backdate, returndate) \
                    SELECT lenddate + ?-7, backdate + ?-7, returndate + ?-7 FROM abklendwork\
                    WHERE lenddate + ?-7 > ? AND backdate + ?-7 < ?;"""
            elif temp:
                sql = """INSERT INTO AttLendWork(lenddate, backdate, returndate) 
                    SELECT lenddate + ?, backdate + ?, returndate + ? FROM abklendwork\
                    WHERE lenddate + ? > ? AND lenddate+ ? < ?;\
                    INSERT INTO attlendwork(lenddate, backdate, returndate) \
                    SELECT lenddate + ?-7, backdate + ?-7, returndate + ?-7 FROM abklendwork\
                    WHERE lenddate + ?-7 > ? AND lenddate + ?-7 < ?;"""

            cursor.execute(sql, wk, wk, wk, wk, beginDate, wk, endDate, wk, wk, wk, wk, beginDate, wk, endDate)
    # 日期筛选整理
    holiday = []
    workday = []
    # yHalf:1，下半学年，0，上半学年，_，未设置
    yHalf = '_'
    for hi in Holiday:
        # 如果开学日期为下半年的日期，跨过元旦，年份应该加一年。
        # 这里突出了日期检查的重要，‘2016-09-02’能够正常工作，其他的诸如‘2016-9-2’，‘09-02-2016’都将不能正常运行，月份格式必须为‘09-02’
        if int(beginDate[5:7]) > 7 and (hi[:2] in ['01', '02']):
            holiday.append(str(int(ny) + 1) + '-' + hi)
            yHalf = '1'
        else:
            holiday.append(str(int(ny)) + '-' + hi)
            yHalf = '0'
    for wi in Workday:
        if int(beginDate[5:7]) > 7 and (wi[:2] in ['01', '02']):
            workday.append(str(int(ny) + 1) + '-' + wi)
        else:
            workday.append(str(int(ny)) + '-' + wi)
    # 先筛选bakcdate为周末或者在holiday数组中的记录，将其删除
    sql = 'DELETE FROM  AttLendWork WHERE datepart(DW, backdate) IN (1,7)'
    cursor.execute(sql)
    rowCount = cursor.rowcount
    for hi in holiday:
        sql = 'DELETE FROM  AttLendWork WHERE CONVERT(VARCHAR(100), backdate, 23) = ?'
        cursor.execute(sql, hi)
        logger.info(rowCount)
        rowCount = rowCount + cursor.rowcount
    tt = 'Delete backdate Effect rows:' + str(rowCount)
    logger.info(tt)
    # 筛选lenddate为周末且不在workday中，将其日期加入数组holiday
    sql = 'SELECT DISTINCT CONVERT(VARCHAR(100), lenddate, 23) FROM  AttLendWork WHERE datepart(DW, lenddate) IN (1,7)'
    cursor.execute(sql)
    for li in cursor:
        if li[0] not in workday and li[0] not in holiday:
            holiday.append(li[0])
    logger.info(holiday)
    # 为workday生成记录，然后删除holiday记录
    for wi in workday:
        t = 0
        wcnt = 0
        for hi in holiday:
            cursor.execute('select datediff(dd,?,?)', wi, hi)
            diff = cursor.fetchone()[0]
            if diff < 30 and diff > 0:
                # 执行日期替换
                sql = 'UPDATE AttLendWork SET lenddate = ? WHERE CONVERT(VARCHAR(100),lenddate,23) = ?'
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
                # sql = 'update AttLendWork set lenddate = ? where did in (select top 30 did from AttLendWork where lenddate = (select top 1 lenddate from AttLendWork where lenddate > ? group by lenddate order by count(lenddate) desc ))'
                # pdb.set_trace()
                sql = 'SELECT TOP 1 CONVERT( VARCHAR(100), lenddate, 23) FROM AttLendWork WHERE lenddate > ? GROUP BY lenddate ORDER BY count(lenddate) DESC'
                cursor.execute(sql, wi)
                tli = cursor.fetchone()[0]
                sql = 'UPDATE AttLendWork SET lenddate = ? WHERE did IN (SELECT TOP 30 did FROM AttLendWork WHERE lenddate = ?)'
                cursor.execute(sql, wi, tli)
                logger.debug('本次替换:')
                wcnt = cursor.rowcount
                logger.debug(wcnt)
                if wcnt > 0:
                    cursor.commit()
            except:
                logger.warn('日期 %s 没有合适的替换日期 ' % wi)
    logger.debug('删除lenddate在holiday中的记录')
    sql = 'DELETE FROM AttLendWork WHERE CONVERT(VARCHAR(100), lenddate, 23) = ?'
    for hi in holiday:
        cursor.execute(sql, hi)
        logger.debug(cursor.rowcount)
    cursor.commit()
    if tmp:
        toperator = '王' + '_00'
    else:
        toperator = '王' + ny[2:4] + yHalf
    # pdb.set_trace()
    cursor.execute('UPDATE AttLendWork SET loperator = ?, boperator = ? WHERE 1=1', toperator, toperator)
    if temp:
        # temp 是一个bool值，当其为真，表示生成的借阅记录仅仅为了应对学期中间的临时检查
        # 将生成的日期池中的backdate > endDate 的backdate 置为 NULL ，同时将boperator也置为NULL
        cursor.execute('UPDATE AttLendWork SET backdate = NULL ,boperator = NULL WHERE backdate >= ?', endDate)
    logger.debug(cursor.rowcount)
    cursor.commit()
    logger.info(hisy)
    # return(hisy)
    # for hi in hisy: