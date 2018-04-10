# --coding: utf-8--

import mysql.connector
import pyodbc

#MYsql configure
my_config = {
        'user':'root',
        'password':'sa',
        'database':'sql-learn'
        }

My_conn = mysql.connector.connect( **my_config )
my_cursor = My_conn.cursor()

#Microsql configure
Mic_config = r'driver={SQL Server};server=localhost;uid=sa;pwd=sa;database=easybook'

mic_conn = pyodbc.connect( Mic_config )
mic_cursor = mic_conn.cursor()

print('import  connection OK!!')



