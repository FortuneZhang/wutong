#coding=utf8
__author__ = 'Administrator'

# import pymssql

# con = pymssql.connect(host='127.0.0.1:1433',user='sa',password='123456',database='test3.db',charset="utf8")
# con = pymssql.connect(host='2012-20140806KE\SQLEXPRESS',user='sa',password='123456',database='test3.db')
# con.close()
# cur = con.cursor()

# cur.execute('select * from test3.dbo.key_value')
# print(cur.fetchall())

import pyodbc
connection = pyodbc.connect('DRIVER={SQL Server};SERVER=2012-20140806KE\SQLEXPRESS;DATABASE=test3;UID=sa;PWD=123456')
cur = connection.cursor()
cur.execute("select * from Table_1")
for row in cur:
    print 'Title:'+row.k,'Content:'+row.v
connection.close()