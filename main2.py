import dpkt, pcap
from dpkt.ip import IP
from dpkt.icmp import ICMP

WUTONGIP = '117.79.156.35'

PcapHandler = pcap.pcap()
PcapHandler.setfilter('tcp')
for ts, buf in PcapHandler:
    eth = dpkt.ethernet.Ethernet(buf)
    srcIp = '%d.%d.%d.%d' % tuple(map(ord, list(eth.data.src)))
    dstIP = '%d.%d.%d.%d' % tuple(map(ord, list(eth.data.dst)))


    if srcIp == WUTONGIP:
        print '---------------'
        ip =eth['data']
        tcp = eth['data']['data']

        print '', srcIp , '->', dstIP
        print tcp['data']

