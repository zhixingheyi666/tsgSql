# --coding: utf-8--
#已经运行过，此为存档文件，若仍需运行，请重新检查参数。并把下面两行退注释
import mysql.connector
import pyodbc


#MYsql configure
my_config = {
        'user':'root',
        'password':'sa',
        'database':'sql-learn'
        }
booklist_wmy = 'insert into booklist( ISBN, BCid, Title, Writer, Epitome, Pages, Price, PublishDate, PageMode, Version, extName, translator, keyword, PubID, Number, frameNo, EnterDate, BcidSn, cbm, cbzz, PYTitle, PYWriter, PYTitleSZ ) values( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )'


My_conn = mysql.connector.connect( **my_config )
my_cursor = My_conn.cursor()

#Microsql configure
Mic_config = r'driver={SQL Server};server=localhost;uid=sa;pwd=sa;database=easybook'

mic_conn = pyodbc.connect( Mic_config )
mic_cursor = mic_conn.cursor()
loop = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 
 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
 'y', 'z']
sql0 = 'select * from booklist where bcid like \''
sql1 = '%\''
#
for yy in loop:
    temp = input("press N to quit:\n")
    if temp == 'N':
        break
    sql_e = sql0 + yy + sql1
    mic_cursor.execute( sql_e )
    mic_rows = mic_cursor.fetchall()
    count_t = 0
    for row in mic_rows:
        print(row)
        print(yy)
        continue
        arg_wmy = []
        for row_mem in row:
            arg_wmy.append( row_mem )
        my_cursor.execute( booklist_wmy, arg_wmy )
        count_t += 1
    My_conn.commit()
    print( count_t )
    print( '\n' )


