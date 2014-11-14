#coding=utf-8
import pcap
import dpkt,re,time




def TryPrintKeyValue(Arr, Key, PrefixStr="", SuffixStr=""):
    try:
        print PrefixStr + Arr[Key] + SuffixStr
    except KeyError:
        pass

def RtnKeyValueNotEmpty(Arr, *Keys):
    for key in Keys:
        try:
            Arr[key]
        except KeyError:
            Arr[key] = ""
    return Arr

PcapHandler = pcap.pcap()
PcapHandler.setfilter('tcp')
for ts, buf in PcapHandler:
    eth = dpkt.ethernet.Ethernet(buf)
    srcIp = '%d.%d.%d.%d' % tuple(map(ord, list(eth.data.src)))
    dstIP = '%d.%d.%d.%d' % tuple(map(ord, list(eth.data.dst)))
    ip = eth.data
    # print ip
    tcp = ip.data
    print '-------' * 8
    print tcp


    # if tcp.dport == 80 or 443 and len(tcp.data) > 0:
    #     # noinspection PyBroadException
    #     try:
    #         http = dpkt.http.Request(tcp.data)
    #         PostData = http.pack()
    #         if len(http.headers):
    #             r = re.findall("user=([\s\S]+?)&(domain=[\s\S]+?)?&password=([\s\S]+?)&", PostData)
    #             if r:
    #                 EmailName = r[0][0]
    #                 Domain = r[0][1]
    #                 EmailPwd = r[0][2]
    #                 UserName = EmailName
    #                 if Domain:
    #                     EmailName += "@" + Domain[8:]
    #             else:
    #                 EmailName = ""
    #                 EmailPwd = ""
    #                 UserName = ""
    #             if True:
    #                 print "[!]================{0:s}===============".format(time.ctime())
    #                 print "IP:{0:s}".format(srcip)
    #                 TryPrintKeyValue(http.headers, "user-agent", "User-agent:")
    #                 TryPrintKeyValue(http.headers, "host", "Host:")
    #                 TryPrintKeyValue(http.headers, "cookie", "Cookie:")
    #                 TryPrintKeyValue(http.headers, "referer", "Referer:")
    #                 print
    #                 print
    #             if True:
    #                 headers = RtnKeyValueNotEmpty(http.headers, "user-agent", "host", "cookie", "referer")
    #                 CurrentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    #                 # time_in,srcip,host,url,postdata,email,username,password,cookie,useragent,referer
    #                 param = (CurrentTime,
    #                          srcip,
    #                          headers["host"],
    #                          http.uri,
    #                          http.pack(),
    #                          EmailName,
    #                          UserName,
    #                          EmailPwd,
    #                          headers["cookie"],
    #                          headers["user-agent"],
    #                          headers["referer"])
    #
    #                 #Log(http.headers, LogFilePath, "user-agent", "host", "cookie", "referer")
    #     except:
    #         print "[!]HTTP analysis exited!"

