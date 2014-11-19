from NetworkAndSync import Sync

__author__ = 'Administrator'
from Queue import Queue
import threading, re, pyodbc, copy
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


class WutongRequestInfo(threading.Thread):
    def __init__(self, sql_server_driver, param_config):
        threading.Thread.__init__(self)
        self.sql_server_driver = sql_server_driver
        self.param_config = param_config
        self.url = 'http://soft.chinawutong.com/DisInfo.ashx'
        self.sync = Sync.HttpSync()
        # http://soft.chinawutong.com/DisInfo.ashx
        # ShellPwd=jftpwTuk6tfUhhWjSDJeeA==&UserID=1481214&UserName=longcreate&DataID=1794412&CheID=218521&Type=Che


    def _analyze_che_info_to_dict(self, che_info, item):
        (pref_email, after_email) = che_info.split('@Email=')
        info = {x.split('=')[0]: x.split('=')[1] for x in pref_email.split('@') if x != ''}
        after_email_array = after_email.split('@')
        if '.' in after_email_array[1]:
            info['Email'] = after_email_array[0] + after_email_array[1]
            print after_email_array[2:]
            info.update({x.split('=')[0]: x.split('=')[1] for x in after_email_array[2:] if x != ''})
        else:
            info.update({x.split('=')[0]: x.split('=')[1] for x in che_info.split('@')})
        info['che_id'] = item[1]
        del (info['ICQ'])
        return info

    def _build_che_info_sql(self, che_info, item):
        info = self._analyze_che_info_to_dict(che_info, item)

        keys = []
        values = []
        for key, value in info.iteritems():
            keys.append('"' + key + '"')
            values.append("'" + value + "'")

        sql = 'INSERT INTO dbo.wutong_che ( '
        sql += ' , '.join(keys)
        sql += ' ) values( '
        sql += ' , '.join(values)
        sql += ' ) '
        return sql.decode('utf-8')

    def run(self):
        item = self.get_one_item()
        if item:
            if item[1] == 0:
                pass
                # che_info = self.get_huo_info(item[0])
            else:
                che_info = self.get_che_info(data_id=item[0], che_id=item[1])
                sql = self._build_che_info_sql(che_info, item)

                conn = self.sql_server_driver.getConnection(sql)
                conn.cursor()


    def get_one_item(self):
        conn = self.sql_server_driver.getConnection()
        cursor = conn.cursor()
        sql = 'select data_id,che_id from dbo.wutong_list where isGetCheDetail = 0 and che_id not in (select che_id from dbo.wutong_che where id != 0)  '
        cursor.execute(sql)
        row = cursor.fetchone()
        cursor.close()
        return row

    def get_che_info(self, data_id, che_id):
        print(self.param_config)
        p = copy.deepcopy(self.param_config)
        p['DataID'] = data_id
        p['Type'] = 'Che'
        p['CheID'] = che_id

        return self.sync.post(self.url, p)

    def get_huo_info(self, data_id):
        params = copy.deepcopy(self.param_config)
        params['DataID'] = data_id
        params['Type'] = 'Huo'

        return self.sync.post(self.url, params)