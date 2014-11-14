__author__ = 'Administrator'
import threading,time
from wutong.wutong import WuTongHandler
class HandleDataQueue(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.wutong = WuTongHandler()

    def run(self):
        # print 'thead run'
        while True:
            if self.queue.empty() is not True:
                # print 'not empty'
                data = self.queue.get()
                if(data['source'] == self.wutong.name):
                    self.wutong.handle(data['data'])
            else:
                # print 'sleep'
                time.sleep(5)