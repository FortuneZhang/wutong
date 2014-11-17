#coding=utf8
__author__ = 'Administrator'

# import pymssql

# con = pymssql.connect(host='127.0.0.1:1433',user='sa',password='123456',database='test3.db',charset="utf8")
# con = pymssql.connect(host='2012-20140806KE\SQLEXPRESS',user='sa',password='123456',database='test3.db')
# con.close()
# cur = con.cursor()

# cur.execute('select * from test3.dbo.key_value')
# print(cur.fetchall())
import sys
import pyodbc
#
# reload(sys)
# sys.setdefaultencoding('utf8')


connection = pyodbc.connect('DRIVER={SQL Server};SERVER=2012-20140806KE\SQLEXPRESS;DATABASE=test3;UID=sa;PWD=123456',charset="UTF-8")
cur = connection.cursor()

# sql = 'INSERT INTO dbo.wutong_list ( "weight" , "allcount" , "CertCarCode" , "tocity" , "id" , "size" , "huodanwei" , "frompro" , "UserType" , "data_type" , "Soft_VIP" , "addtime" , "fromarea" , "fromcity" , "cust_id" , "endtime" , "leixing" , "shuoming" , "name" , "kind" , "prize" , "toarea" , "data_id" , "che_id" , "topro" , "jingguo" , "shuliang" ) values( '.decode('utf-8').encode('utf-8')
# sql += "'35' , '1000' , '' , '苏州市' , '54963828' , '17' , '' , '福建省' , '' , '2' , '1' , '2014-11-17 15:02:34' , '长乐市' , '福州市' , '1479217' , '2014-11-17 15:02:34' , '' , '求货源' , '皖K05992' , '回程车' , '1' , '市辖区' , '1802564' , '218523' , '江苏省' , '' , '' )".decode('utf-8').encode('utf-8')
# print sql
sql = 'insert into dbo.Table_1("v", "k") values(' + "'张三那', 'b')".decode('utf-8')
print sql

# cur.execute("select * from dbo.wutong_list where iid = 1" )
try:
    cur.execute(sql)
    cur.commit()
except Exception ,e:
    print str(e).encode('utf-8').decode('gbk')
# for row in cur:
#     print row
connection.close()