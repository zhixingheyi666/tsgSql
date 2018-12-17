# -*- coding: utf-8 -*-
"""
define interface to Mysql, make connection
"""

#import pymysql
from mysql import connector

from pyodbc import connect

"""
if the LOG_sf exist in the current package, just using "import LOG_sf", or codes below
"""
try:
    from .LOG_sf import logger
#from fc.LOG_sf import logger
except Exception as e:
    print(e)
    from testlog.LOG_sf import logger
try:
    pass
except:
    pass 

#from python_learn.LOG_eg import logger
conn_SQL_tools = ( 'cursor',
    'pd:pagedown',
    'pall:pagedown',
    'mkcon: build connection to sql, default mysql, \'mic\' for sql 2000')

mconf = {
        'user': 'root',
        'password': 'sa',     
        'database': 'spider'       
        }

micfg = r'driver={SQL Server};server=localhost;uid=sa;pwd=sa;database=easybook'
def mkcon( s = 'my'):
    try:
        if s == 'my':
            mconn = connector.connect( **mconf )
            logger.info( 'Building connection to Mysql...' )
        elif s == 'mic':
            mconn = connect( micfg )
            logger.info( 'Building connection to Micsql...' )
        else:
            raise Exception( 'Bad config for make connection to SQL' ) 
        cursor = mconn.cursor()
    except:
        logger.exception( 'Failure Information!' )
        logger.info( 'CONN Failure!' )
    return ( cursor, mconn ) 
def pd( cursor, b = 10 ):
    rows = cursor.fetchmany( b )
    logger.debug( 'rows:' + str(len(rows)))
    for i in rows:
        logger.info( i )
    return rows

def pall( cursor ):
    rows = cursor.fetchall()
    logger.debug( 'rows:' + str(len(rows)))
    for i in rows:
        logger.info( i )
    return rows




    
