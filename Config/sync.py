__author__ = 'Administrator'
import json
import urllib2, urllib, httplib


class HttpSync(object):
    def __init__(self):
        pass

    @staticmethod
    def post(self, url, params):
        req = urllib2.Request(url)
        data = urllib.urlencode(params)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, data)
        return response.read()

