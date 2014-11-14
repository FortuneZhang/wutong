__author__ = 'Administrator'
from Queue import Queue
import threading, re


class WuTongReceiver():
    def __init__(self, queue):
        self.queue = queue
        self.data = ''
        self.name = 'wutong'


    def receive(self, data):
        if '@' in data:
            self.data += data
        # print 'receiver data'
        if data.endswith('</Data>'):
            self.queue.put({'source': self.name, 'data': self.data})
            data = ''
            # print 'insert queue and data is blank'


class WuTongHandler():
    def __init__(self):
        self.name = 'wutong'
        self.db = WuTongDB()

    def handle(self, data):
        print 'handle'
        threading.Thread(target=self._handle, args=(data,)).start()

    def _handle(self, data):
        print '_handle'
        # print data
        items = re.findall('<Data>([^<]+)</Data>', data)
        for item in items:
            itemJosn = {x.split('=')[0]: x.split('=')[1] for x in item.split('@@@@@@') if '=' in x}
            self.db.receive(itemJosn)


class WuTongDB():
    def __init__(self):
        self.name = 'wutong'

    def receive(self, data):
        sql = self._build_sql(data)

    def _build_sql(self, data):
        # print data
        # print data.keys()
        # print data.values()
        keys = []
        values = []
        for key, value in data.iteritems():
            keys.append('"' + key + '"')
            values.append("'" + value + "'")

        sql = 'INSERT INTO wutong_list ( '
        sql += ' , '.join(keys)
        sql += ' ) values( '
        sql += ' , '.join(values)
        sql += ' ) '
        return sql




class WuTongNet():
    def __init__(self):
        self.name = 'wutong'