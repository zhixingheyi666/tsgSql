# --coding: utf-8--
#已经运行过，此为存档文件，若仍需运行，请重新检查参数。并把下面两行退注释
#import mysql.connector
#import pyodbc

#MYsql configure
my_config = {
        'user':'root',
        'password':'sa',
        'database':'sql-learn'
        }
lendwork_wmy = 'insert into lendwork( rid, bcid, lenddate, returndate, backdate, loperator, boperator, bid ) values( %s, %s, %s, %s, %s, %s, %s, %s )'

My_conn = mysql.connector.connect( **my_config )
my_cursor = My_conn.cursor()

#Microsql configure
Mic_config = r'driver={SQL Server};server=localhost;uid=sa;pwd=sa;database=easybook'

mic_conn = pyodbc.connect( Mic_config )
mic_cursor = mic_conn.cursor()

yearlist = [ '2011', '2012', '2013', '2014', '2015', '2016' ]
sql0 = 'select * from lendwork where year(lenddate) ='

for yy in yearlist:
    temp = input("press N to quit:\n")
    if temp == 'N':
        break
    sql_e = sql0 + yy
    mic_cursor.execute( sql_e )
    mic_rows = mic_cursor.fetchall()
    count_t = 0
    for row in mic_rows:
#    print(row)
        arg_wmy = []
        for row_mem in row:
            arg_wmy.append( row_mem )
        my_cursor.execute( lendwork_wmy, arg_wmy )
    My_conn.commit()
    count_t += 1
    print( count_t )
    print( '\n' )


