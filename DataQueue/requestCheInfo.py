# coding=utf-8
from config.db import SQLServerDriver, Config
from wutong.wutong import WutongRequestInfo


class RequestCheInfo():
    def __init__(self):
        self.sql_server_driver = SQLServerDriver()
        self.config = Config()


    def run(self):
        wutong_request_info = WutongRequestInfo(self.sql_server_driver, self.config.get_sync_param())
        wutong_request_info.start()




