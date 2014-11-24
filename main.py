# coding=utf-8
import dpkt, pcap
from Queue import Queue
from wutong.wutong import *
from dataQueue.handleLists import HandleDataQueue
from dataQueue.requestCheInfo import RequestCheInfo
from config.db import SQLServerDriverConnectionPoll

class Main():
    def __init__(self):
        self.queue = Queue()

        self.PcapHandler = pcap.pcap()
        self.PcapHandler.setfilter('tcp')

        self.WUTONGIP = '117.79.156.35'
        self.wenkong = WuTongReceiver(self.queue)
        self.queueHandler = HandleDataQueue(self.queue)
        self.requestCheInfo = RequestCheInfo()
    def main(self):

        self.requestCheInfo.run()
        self.queueHandler.start()
        for ts, buf in self.PcapHandler:
            eth = dpkt.ethernet.Ethernet(buf)
            srcIp = '%d.%d.%d.%d' % tuple(map(ord, list(eth.data.src)))
            dstIP = '%d.%d.%d.%d' % tuple(map(ord, list(eth.data.dst)))


            if srcIp == self.WUTONGIP:

                self.wenkong.receive(eth['data']['data']['data'])



if __name__ == '__main__':
    # main = Main()
    # main.main()

    print 'init....'
    poll = SQLServerDriverConnectionPoll.get_instance()

    conn1 =  poll.lend()
    conn2 =  poll.lend()
    print conn1
    print conn2
    print conn1['idx']

    poll.restore(conn1['idx'])

