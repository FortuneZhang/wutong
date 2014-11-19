__author__ = 'Administrator'

import pyodbc, os


class SQLServerDriver():
    def __init__(self):
        self.connection = ''
        self.config = Config()


    def getConnection(self):
        db = self.config.getDb();
        conn_str = 'DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (
            db['SERVER_NAME'], db['DATABASE'], db['UID'], db['PWD'])
        self.connection = pyodbc.connect(conn_str, charset="UTF-8")
        return self.connection


    def closeConnection(self):
        self.connection.close()


class Config():
    DB = {
        'SERVER_NAME': '',
        'DATABASE': '',
        'UID': '',
        'PWD': ''
    }

    SYNC_PARAM = {
        'ShellPwd': 'jftpwTuk6tfUhhWjSDJeeA==',
        'UserID': '1481214',
        'UserName': 'longcreate'
    }
    syncInterval = 10


    def __init__(self):
        self.is_read = False

    def _read_config_file(self):
        self.is_read = True
        file = os.path.join(os.getcwd() + '\\' + 'config.cfg')
        f = open(file)
        for line in f.readlines():
            if line == '' or line.startswith('//'):
                pass
            else:
                c = line.split(' ')
                if c[0] in self.__class__.DB.keys():
                    self.__class__.DB[c[0]] = c[1].strip()
                if c[0] in self.__class__.SYNC_PARAM.keys():
                    self.__class__.SYNC_PARAM[c[0]] = c[1].strip()
                elif c[0] == 'syncInterval':
                    try:
                        self.__class__.syncInterval = int(c[1].strip())
                    except:
                        print 'cant load syncInterval'

        f.close()

    def getSyncInterval(self):
        if not self.is_read:
            self._read_config_file()
        return self.__class__.syncInterval

    def getDb(self):
        if not self.is_read:
            self._read_config_file()
        return self.__class__.DB

    def get_sync_param(self):
        if not self.is_read:
            self._read_config_file()
        return self.__class__.SYNC_PARAM
