__author__ = 'Administrator'

import pyodbc
class SQLServerDriver():
    def __init__(self):
        self.connection = ''


    def getConnection(self):
        self.connection =  pyodbc.connect('DRIVER={SQL Server};SERVER=2012-20140806KE\SQLEXPRESS;DATABASE=test3;UID=sa;PWD=123456',charset="UTF-8")
        return self.connection


    def closeConnection(self):
        self.connection.close()
