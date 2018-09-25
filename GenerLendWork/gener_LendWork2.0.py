# -*- coding: utf-8 -*-


import random, pdb
from itertools import zip_longest as myzip

from fc.conn_SQL import *
from fc.LOG_sf import logger

cursor, mkconn = mkcon('mic')

from RidBidDate import Rid, Bid, lDay

"""
rid:读者id,也就是借书证号,数据库中每一个id号和一个读者一一对应
bid:书籍id,每一个id号和唯一的一本书一一对应
lDay: lendDay,生成借阅记录中日期部分的函数
        内容包括借书操作员(loperator),还书操作员(boperator)
        借出日期(lenddate),还书日期(backdate),应还日期(returndate)
"""


def gener(beginDate, endDate, Holiday, Workday, yearBefore, times=5, Reader='All', tmp=False, temp=False, tempNum=0):
    """
    :param beginDate: 要生成借阅记录的起始时间,一般为学期开始 格式为: yyyy-mm-dd
    :param endDate: 要生成的借阅记录的结束时间 格式为: yyyy-mm-dd
    :param Holiday: 在 beginDate 和 endDate 之间的法定节假日,例如十一假期,中秋节等
                    格式为: [mm-dd,mm-dd,...] 是一个list,每年不尽相同,要根据实际调整
    :param Workday: 在 beginDate 和 endDate 之间法定节假日调休而产生的工作日
                    格式为: [mm-dd,mm-dd,...] 是一个list,每年不尽相同,要根据实际调整
    :param yearBefore: 如果为0,表示生成本学年度的借阅记录.
                        (一个学年度两个学期，从一个暑假到另一个暑假之间的时间
                         同一学年度内，学生的年级不会发生变化，如果进入下一学年度，学生的年级将
                         升高一级，例如从五年级升入六年级)
                        如果值为n,表示生成从当前年份向前数第n年的借阅记录.
    :param times:   典型值是一个学期4次,表示在起始和结束日期之间,平均为每个学生生成times条借阅记录.
    :param tempNum: 参数用于决定需要生成多少条借阅记录，可以在配置文件config.py中设定
                        例如：用于20171016借阅记录生成条目总数的限制，开学仅仅一个半月，限制在960条吧
                        此时可以设置tempNum = 960,那么仅仅会有960条生成的记录写入数据库
    :param Reader: 留用
    :param tmp: 测试程序时,或者学期中间检查，生成一些临时记录,将其值置为1.此时生成的借阅记录的loperator为<王_00>.
                    测试完毕,可用  "delete from LendWork where loperator='王_00'"  语句仅将测试数据删除.
                    ·注意在sql中，字符串是用单引号包围起来的部分，如果用双引号或者反引号包围，
                        那么表示的是列名，例如同样是上面的句子，如果这样写
                            delete from LendWork where loperator="王_00"
                        就会报找不到列名 王_00 的错误
    :param temp: (会生成部分未归还记录)通常是按整个学期生成借阅记录,如果学期还未结束,有检查的来,需要临时生成一些借阅
                    记录,将此参数置为Ture,则可以生成一些<未归还>的书籍,让生成的结果更逼真.
                    bug:有学生会在重叠的时间段内借阅两本书,以后可以在最后再加一个筛选函数解决
     :gStat:  函数状态标志，以后每个函数都应包含名为Stat的函数状态标志
    :return: None   or   gStat(函数状态标志，以后每个函数都应包含名为Stat的函数状态标志)
    """
    # 参数范围校验
    if yearBefore > 5 or yearBefore < 0 or type(yearBefore) is not int:
        gStat = ['yearBefore:如果生成本学年的，值为0，如果生成上个学年的借阅记录，值为1，上上个学年，值为2，依次类推', 'yearBefore参数错误', False]
        logger.warn(gStat)
        return gStat
    """
    tGrade: 各年级的times,平均借阅次数
        这里如果从前曾经借过的书越多，这个年级生成的条目占比就越多，如此循环，最后可致比例失衡，下面加入比例控制因子
        一年级生均2.5，二年级3.5，三4，四4.5，五5.5，六4
        总记录数 = 一年级人数 * 2.5 + 二年级人数 * 3.5 +三年级人数 * 4 +四年级人数 * 4.5 +五年级人数 * 5.5 +六年级人数 * 4
    """
    bidInuse = set()
    times = times/4
    tGrade = [['一', 2.5*times], ['二', 3.5*times], ['三', 4*times], ['四', 4.5*times], ['五', 5.5*times], ['六', 4*times]]
    if yearBefore == 0:
        tGrid = tGbid = tGrade
    else:
        """
        这里的巧妙写法，应该添加详细注释
        下面的语句中，会把tGrid和tGbid对应起来，加入yearBefore的值为1
        则tGrid的序列是二三四五六，
          tGbid的序列是一二三四五，
          rid表示的是读者目前分别就读于二三四五六年级，那么1年以前，
          他们所在的年级应当是一二三四五年级，所以那个时间，他们应当
          借阅的书籍应该分别是从前一二三四五年级学生借阅过的书籍，所以
          tGbid就选一二三四五，
        """
        tGrid = tGrade[yearBefore:]
        tGbid = tGrade[: -yearBefore]
    ttRidBid = []
    trid_num = 0
    for tgR, tgB in myzip(tGrid, tGbid):
        # 选取需要生成借阅记录的读者(当前数据库内的真实读者)
        rid = Rid(tgR[0])
        rL = len(rid)
        if rL == 0:
            logger.warn('@@@未找到任何  %s年级  读者。' % tgR[0])
            continue
        trid_num = trid_num + rL
        # 选取恰当的书籍(bid),如上面选取的读者是在选定的时间期间,就读于五年级,则应选取五年级曾经借阅过的书籍
        bid = Bid(tgB[0])
        bL = len(bid)
        if (bL <= rL):
            return False
        # 让读者(rid)倍增到与bid(bL)数目相等
        rid = rid * (bL // rL + 1)
        # shuffle(rid),对rid进行随机排序(打乱顺序)
        random.shuffle(rid)
        random.shuffle(bid)
        rid = rid[:bL]
        # 如果bid数目大于每个年级预设的平均借阅次数(tgB[i])与读者数(rL)的乘积,重设rL
        # round(x),对x进行四舍五入
        if bL > rL * tgB[1]:
            bL = round(rL * tgB[1])
        for i in range(bL):
            ti = bid[i] + [rid[i]]
            ttRidBid.append(ti)
    random.shuffle(ttRidBid)
    logger.debug('生成日期条目:')
    lDay(beginDate, endDate, Holiday, Workday, tmp, temp)
    """
    读者、日期匹配规则：
          先把所有lenddate出现次数少于50的记录全匹配一遍（避免日期丢失问题），然后剩余读者的按概率随机匹配
    """
    try:
        sql = 'SELECT count(lenddate) cn,CONVERT(VARCHAR(100), lenddate, 23) lenddate INTO #t1 FROM AttLendWork GROUP BY lenddate'
        cursor.execute(sql)
    except:
        cursor.execute('TRUNCATE TABLE #t1')
        sql = 'INSERT INTO #t1 SELECT count(lenddate) cn,CONVERT(VARCHAR(100), lenddate, 23) lenddate FROM AttLendWork GROUP BY lenddate'
        cursor.execute(sql)
    sql = 'SELECT did FROM AttLendWork WHERE CONVERT(VARCHAR(100), lenddate, 23) IN (SELECT lenddate FROM #t1 WHERE cn < 50)'
    cursor.execute(sql)
    Adid = set()
    for ci in cursor.fetchall():
        Adid.add(ci[0])
    tnum = len(ttRidBid) - len(Adid)
    if tnum > 0:
        # --从剩余的日期条目随机抽取匹配读者条目,先抽取3倍需要量，再截取
        # pdb.set_trace()
        sql = 'select top %s did from AttLendWork order by checksum(newid())' % (str(tnum * 3))
        cursor.execute(sql)
        Bdid = set()
        for ci in cursor.fetchall():
            Bdid.add(ci[0])
        Cdid = list(Bdid - Adid)
        random.shuffle(Cdid)
        # 汇聚所有用于生成记录的日期条目
        Ddid = Cdid[:tnum] + list(Adid)
    else:
        Ddid = list(Adid)
    Ddid.sort()
    tLendWork = []
    for i in range(len(ttRidBid)):
        ttRidBid[i].append(Ddid[i])
        tLendWork.append(tuple(ttRidBid[i]))
    # 学期中间检查，前面生成的记录过多，下面语句用于截取部分数据。
    # 例如：用于20171016借阅记录生成条目总数的限制，开学仅仅一个半月，限制在960条吧
    # tempNum 参数用于决定需要生成多少条借阅记录，可以在配置文件config.py中设定
    if temp:
        random.shuffle(tLendWork)
        tLendWork = tLendWork[:tempNum]
    # pdb.set_trace()
    logger.info('预备有 %s 条记录写入LendWork' % len(tLendWork))
    sql = 'INSERT INTO LendWork( bid, Bcid, Rid, LendDate, ReturnDate, BackDate, loperator, boperator ) SELECT ?, ?, ?, LendDate, ReturnDate, BackDate, loperator, boperator FROM AttLendWork WHERE did = ?'
    cursor.executemany(sql, tLendWork)
    cursor.commit()
    logger.info('Success!')


if __name__ == '__main__':
    """
    1.主程序需要的参数写在config模块中,并且以函数的返回值(kw)的方式传递回主程序
    2.这里用了一个option,因为每次生成借阅记录,都要重新组织日期参数,
    传递一个option给getConfig,用来选择相应的日期参数
    """
    from config import getConfig
    option = 20180926
    kw = getConfig(option)
    if kw == -1:
        logger.warn('Break in function getConfig!')
    else:
        gener(**kw)
