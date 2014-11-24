# coding=utf-8
from NetworkAndSync import Sync
import time

__author__ = 'Administrator'
import threading, re, pyodbc, copy
from config.db import SQLServerDriver


class WuTongReceiver():
    def __init__(self, queue):
        self.queue = queue
        self.data = ''
        self.name = 'wutong'


    def receive(self, data):
        print u'接受到来自wutong的数据'
        if '@' in data:
            self.data += data
        if data.endswith('</Data>'):
            self.queue.put({'source': self.name, 'data': self.data})
            print u'已经将数据加入到队列中，等待处理'
            data = ''


class WuTongHandler():
    def __init__(self):
        self.name = 'wutong'
        self.db = WuTongDB()

    def handle(self, data):
        print u'准备进行数据处理'
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
        print u'准备进行数据处理'

        conn = self.dbDriver.getConnection()
        cursor = conn.cursor()
        print u'查看数据库中是否存在这条数据'
        check_is_exist_sql = 'select iid from wutong_list where  id = %s' % (data['id'])
        cursor.execute(check_is_exist_sql)
        row = cursor.fetchone()
        if not row:
            print u'不存在相同数据，将数据插入到数据库中。'
            sql = self._build_sql(data)
            print sql
            cursor.execute(sql)
            cursor.commit()
        else:
            print u'已经存在相同的数据，越过处理。。。'
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
        print che_info
        (pref_email, after_email) = che_info.split('@Email=')
        info = {x.split('=')[0]: x.split('=')[1] for x in pref_email.split('@') if x != ''}
        after_email_array = after_email.split('@')
        if '.' in after_email_array[1]:
            info['Email'] = after_email_array[0] + after_email_array[1]
            info.update({x.split('=')[0]: x.split('=')[1] for x in after_email_array[2:] if x != ''})
        elif '=' not in after_email_array[0]:
            info['Email'] = after_email_array[0]
            info.update({x.split('=')[0]: x.split('=')[1] for x in after_email_array[1:] if x != ''})
        else:
            info.update({x.split('=')[0]: x.split('=')[1] for x in che_info.split('@')})
            info['Email'] = ''
        info['che_id'] = item[1]
        del (info['ICQ'])
        return info

    def _build_che_info_sql(self, che_info, item):
        print u'分析che数据'
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
        print(u'构建che sql')
        print info
        return sql

    def __analyze_huo_info_to_dict(self, huo_info, item):
        info = {x.split('=')[0]: x.split('=')[1] for x in huo_info.split('@') if x != ''}
        info['list_iid'] = item[0]
        del (info['ICQ'])
        return info

    def _build_huo_info_sql(self, huo_info, item):
        print u'分析huo数据'
        d = self.__analyze_huo_info_to_dict(huo_info, item)
        keys = []
        values = []
        for key, value in d.iteritems():
            keys.append('"' + key + '"')
            values.append("'" + value + "'")
        sql = 'INSERT INTO dbo.wutong_huo ( '
        sql += ' , '.join(keys)
        sql += ' ) values( '
        sql += ' , '.join(values)
        sql += ' ) '
        print u'构建huo数据'
        return sql

    def run(self):
        while True:
            time.sleep(1)
            print u'查找下一条需要请求的条目'
            item = self.get_one_item()
            print 'item->', item
            if item:
                conn = self.sql_server_driver.getConnection()
                cursor = conn.cursor()
                if item[1] == '0' or item[1] == '':
                    huo_info = self.get_huo_info(item[0])
                    print huo_info
                    huo_sql = self._build_huo_info_sql(huo_info.decode('utf8'), item)
                    cursor.execute(huo_sql)
                    cursor.commit()
                    conn.close()
                else:
                    che_info = self.get_che_info(data_id=item[0], che_id=item[1])
                    print che_info
                    che_sql = self._build_che_info_sql(che_info.decode('utf8'), item)
                    cursor.execute(che_sql)
                    cursor.commit()
                    conn.close()
                print u'更新列表中，尚未设置标记字段的'
                self.update_list_item_has_info(item[2])

            else:
                time.sleep(10)

    def update_list_item_has_info(self, iid):
        sql = 'update dbo.wutong_list set isGetCheDetail =1 where iid = %s' % (iid)
        conn = self.sql_server_driver.getConnection()
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.commit()
        conn.close()

    def get_one_item(self):
        conn = self.sql_server_driver.getConnection()
        cursor = conn.cursor()

        sql_list = "select top 1 data_id,che_id, iid from dbo.wutong_list where isGetCheDetail = 0 "
        # print 'before while '
        while True:
            cursor.execute(sql_list)
            row_list = cursor.fetchone()
            # print 'row_list->', row_list
            if row_list is None:
                print u'没有需要请求的详细信息，进入休息队列，10秒后继续。'
                time.sleep(10)
                continue

            if row_list[1] == '0' or row_list[1] == '':
                print u'找到一条需要请求的车队，正在处理'
                break
            else:
                sql_che = 'select iid from  dbo.wutong_che where che_id  = %s ' % (row_list[1])
                cursor.execute(sql_che)
                row_che = cursor.fetchone()
                # print 'row_che--> ', row_che
                if row_che is not None:
                    # print  'is not None'
                    sql = 'update dbo.wutong_list set isGetCheDetail =1 where iid = %s' % (row_list[2])

                    cursor.execute(sql)
                    cursor.commit()
                else:
                    # print  'is None'
                    break

        conn.close()

        return row_list

    def get_che_info(self, data_id, che_id):
        print u'请求che详细信息'
        p = copy.deepcopy(self.param_config)
        p['DataID'] = data_id
        p['Type'] = 'Che'
        p['CheID'] = che_id

        return self.sync.post(self.url, p)

    def get_huo_info(self, data_id):
        print u'请求huo详细信息'
        params = copy.deepcopy(self.param_config)
        params['DataID'] = data_id
        params['Type'] = 'Huo'

        return self.sync.post(self.url, params)