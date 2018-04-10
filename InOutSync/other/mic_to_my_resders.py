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
reader_wmy = 'insert into reader( name, rid, depid, picture, isfine, isgs, isfinish, rgid, guestpassword, iddisp ) values( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )'

My_conn = mysql.connector.connect( **my_config )
my_cursor = My_conn.cursor()

#Microsql configure
Mic_config = r'driver={SQL Server};server=localhost;uid=sa;pwd=sa;database=easybook'

mic_conn = pyodbc.connect( Mic_config )
mic_cursor = mic_conn.cursor()

reader_rmic = '"select * from reader limit 10"'

mic_cursor.execute("select * from reader")
mic_rows = mic_cursor.fetchall()
count_t = 0
for row in mic_rows:
#    print(row)
    arg_wmy = []
    for row_mem in row:
        arg_wmy.append( row_mem )
    my_cursor.execute( reader_wmy, arg_wmy )
    My_conn.commit()
    count_t += 1
print( count_t )


