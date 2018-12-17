# _*_coding:utf-8_*_
"""
1.为了主程序简洁清楚,主程序需要的参数写在这个模块中,并且以函数的返回值(kw)的方式传递回主程序
2.这里用了一个option,因为每次生成借阅记录,都要重新组织日期参数,
    从主程序传递一个option,用来选择相应的日期参数
"""
from fc.LOG_sf import logger

__author__ = 'Master Wang'


def getConfig(option):
    """
    :param option: 运行<生成借阅记录程序>的日期 格式为: yyyymmdd
    :return: dict,事先在这里编写好的参数
    :param tempNum: 参数用于决定需要生成多少条借阅记录，可以在配置文件config.py中设定
                        例如：用于20171016借阅记录生成条目总数的限制，开学仅仅一个半月，限制在960条吧
                        此时可以设置tempNum = 960,那么仅仅会有960条生成的记录写入数据库
    :param temp: 由于程序没有添加相应的处理语句，这参数和tempNum两个参数不能省略，
                    当temp设定为False时，tempNum的设定值将不会被程序采用
    ··注意，times参数这里并没有设置接口，如果需要，可以直接修改gener函数对应位置的默认值
    """
    if 1 == 1:
        if option == 20181217:
           bidInuse = set()
           beginDate = '2018-09-03'
           endDate = '2018-12-17'
           holiday = ['09-24', '10-01', '10-02', '10-03', '10-04', '10-05', '10-06', '10-07']
           workday = ['09-29', '09-30']
           yearbefore = 0
           tmp = True
           temp = True
           tempNum = 2200

        if option == 20181112:
            bidInuse = set()
            beginDate = '2018-09-03'
            endDate = '2018-11-16'
            holiday = ['09-24', '10-01', '10-02', '10-03', '10-04', '10-05', '10-06', '10-07']
            workday = ['09-29', '09-30']
            yearbefore = 0
            tmp = True
            temp = True
            tempNum = 1700

        if option == 20181105:
            bidInuse = set()
            beginDate = '2018-09-03'
            endDate = '2018-11-04'
            holiday = ['09-24', '10-01', '10-02', '10-03', '10-04', '10-05', '10-06', '10-07']
            workday = ['09-29', '09-30']
            yearbefore = 0
            tmp = True
            temp = True
            tempNum = 1600

        if option == 20180926:
            bidInuse = set()
            beginDate = '2018-09-03'
            endDate = '2018-09-26'
            holiday = ['09-24']
            workday = []
            yearbefore = 0
            tmp = True
            temp = True
            tempNum = 640

        if option == 20180925:
            bidInuse = set()
            beginDate = '2018-03-05'
            endDate = '2018-06-22'
            holiday = ['04-05', '04-06', '04-07', '04-29', '04-30', '05-01', '05-17', '05-18', '05-16']
            workday = ['04-08', '04-28']
            yearbefore = 1
            tmp = False
            temp = False
            tempNum = 1500

        if option == 20180625:
            bidInuse = set()
            beginDate = '2018-03-05'
            endDate = '2018-06-22'
            holiday = ['04-05', '04-06', '04-07', '04-29', '04-30', '05-01', '05-17', '05-18', '05-16']
            workday = ['04-08', '04-28']
            yearbefore = 0
            tmp = False
            temp = False
            tempNum = 3200

        if option == 20180107:
            bidInuse = set()
            beginDate = '2017-09-04'
            endDate = '2018-01-07'
            holiday = ['10-01', '10-02', '10-03', '10-04', '10-05', '10-06', '10-07', '10-08', '12-30', '12-31', '01-01']
            workday = ['09-30']
            tmp = False
            temp = True
            tempNum = 2800
            yearbefore = 0

        if option == 20171110:
            bidInuse = set()
            beginDate = '2017-09-04'
            endDate = '2017-11-10'
            holiday = ['10-01', '10-02', '10-03', '10-04', '10-05', '10-06', '10-07', '10-08']
            workday = ['09-30']
            tmp = False
            temp = True
            tempNum = 1516
            yearbefore = 0
    try:
        # kw = dict(bidInuse=bidInuse, beginDate=beginDate, endDate=endDate, holiday=holiday, workday=workday, temp=temp)
        kw = dict(beginDate=beginDate, endDate=endDate, Holiday=holiday, Workday=workday, yearBefore=yearbefore, temp=temp, tmp=tmp,tempNum=tempNum)
        return kw
    except BaseException as e:
        print("No option matches,Please check the option string！！")
        logger.warn(e)
        logger.warn("No option matches,Please check the option string！！")
        return -1


"""
    if 1 == 1:
        if option == 20171101:
            bidInuse = set()
            beginDate = '2017-09-04'
            endDate = '2017-11-01'
            holiday = ['10-01', '10-02', '10-03', '10-04', '10-05', '10-06', '10-07', '10-08']
            workday = ['09-30', '05-27']
            tmp = False
            temp = True
            tempNum = 960
            yearbefore = 0
    if 1 == 1:
        if option == 20160706:
            bidInuse = set()
            beginDate = '20-17-02-14'
            endDate = '2017-06-11'
            holiday = ['04-02', '04-03', '04-04', '04-29', '04-30', '05-01', '05-28', '05-29', '05-30']
            workday = ['04-01', '05-27']
    if 1 == 1:
        if option == -1:
            bidInuse = set()
            beginDate = '2017-02-14'
            endDate = '2017-06-11'
            holiday = ['04-02', '04-03', '04-04', '04-29', '04-30', '05-01', '05-28', '05-29', '05-30']
            workday = ['04-01', '05-27']
        if option == 1:
            bidInuse = set()
            beginDate = '2016-09-02'
            endDate = '2017-01-12'
            holiday = ['09-15', '09-16', '09-17', '10-01', '10-02', '10-03', '10-04', '10-05', '10-06', '10-07',
                       '12-31', '01-01', '01-02']
            workday = ['09-18', '10-08', '10-09']
        if option == 1:
            bidInuse = set()
            beginDate = '2016-02-25'
            endDate = '2016-07-05'
            holiday = ['04-02', '04-03', '04-04', '04-30', '05-01', '05-02', '06-09', '06-10', '06-11']
            workday = ['06-12']
        if option == 1:
            bidInuse = set()
            beginDate = '2015-09-01'
            endDate = '2016-01-25'
            holiday = ['09-03', '09-04', '09-05', '09-26', '09-27', '10-01', '10-02', '10-03', '10-04', '10-05',
                       '10-06', '10-07', '01-01', '01-02', '01-03']
            workday = ['09-06', '10-10']
        if option == 1:
            bidInuse = set()
            beginDate = '2015-03-09'
            endDate = '2015-07-03'
            holiday = ['04-04', '04-05', '04-06', '05-01', '05-02', '05-03', '06-20', '06-21', '06-22']
            workday = []
        if option == 1:
            bidInuse = set()
            beginDate = '2014-09-01'
            endDate = '2015-02-05'
            holiday = ['09-05', '09-06', '09-07', '09-26', '09-27', '10-01', '10-02', '10-03', '10-04', '10-05',
                       '10-06', '10-07', '01-01', '01-02', '01-03']
            workday = ['09-28', '10-11', '01-04']
            gener(beginDate, endDate, holiday, workday, yearBefore=2, tmp=0)
        if option == 1:
            bidInuse = set()
            beginDate = '2014-02-17'
            endDate = '2014-07-03'
            holiday = ['04-05', '04-06', '04-07', '05-01', '05-02', '05-03', '05-31', '06-01', '06-02']
            workday = ['05-04']
        if option == 1:
            bidInuse = set()
            beginDate = '2013-09-02'
            endDate = '2014-01-15'
            holiday = ['09-19', '09-20', '09-21', '10-01', '10-02', '10-03', '10-04', '10-05', '10-06', '10-07',
                       '01-01']
            workday = ['09-22', '09-29', '10-12']
        if option == 1:
            bidInuse = set()
            beginDate = '2013-02-18'
            endDate = '2013-07-04'
            holiday = ['04-04', '04-05', '04-29', '04-30', '05-01', '06-10', '06-11', '06-12']
            workday = ['04-07', '04-27', '04-28', '06-08', '06-09']
        if option == 1:
            bidInuse = set()
            beginDate = '2012-09-03'
            endDate = '2013-01-15'
            holiday = ['09-30', '10-01', '10-02', '10-03', '10-04', '10-05', '10-06', '10-07', '01-01', '01-02',
                       '01-03']
            workday = ['09-29', '10-08', '01-05', '01-06']
"""
