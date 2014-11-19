__author__ = 'Administrator'
from Queue import Queue
import threading, re, pyodbc
from config.db import SQLServerDriver


class WuTongReceiver():
    def __init__(self, queue):
        self.queue = queue
        self.data = ''
        self.name = 'wutong'


    def receive(self, data):
        if '@' in data:
            self.data += data
        if data.endswith('</Data>'):
            self.queue.put({'source': self.name, 'data': self.data})
            data = ''


class WuTongHandler():
    def __init__(self):
        self.name = 'wutong'
        self.db = WuTongDB()

    def handle(self, data):
        print 'handle'
        threading.Thread(target=self._handle, args=(data,)).start()

    def _handle(self, data):
        items = re.findall('<Data>([^<]+)</Data>', data)
        for item in items:
            itemJosn = {x.split('=')[0]: x.split('=')[1] for x in item.split('@@@@@@') if '=' in x}
            self.db.receive(itemJosn)


class WuTongDB():
    def __init__(self):
        self.name = 'wutong'
        self.dbDriver = SQLServerDriver()

    def receive(self, data):
        sql = self._build_sql(data)
        conn = self.dbDriver.getConnection()
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.commit()
        self.dbDriver.closeConnection()

    def _build_sql(self, data):
        keys = []
        values = []
        if len(data['name']) < 4:
            print data
        for key, value in data.iteritems():
            keys.append('"' + key + '"')
            values.append("'" + value + "'")

        sql = 'INSERT INTO dbo.wutong_list ( '
        sql += ' , '.join(keys)
        sql += ' ) values( '
        sql += ' , '.join(values)
        sql += ' ) '
        return sql.decode('utf-8')



class WuTongNet():
    def __init__(self):
        self.name = 'wutong'