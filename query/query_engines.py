#!/usr/bin/env python
# encoding: utf-8

import gtaskpool
from proxymanager.downloadproxylist import get_http_proxies
from proxymanager.downloadualist import get_useragents
from proxymanager.proxymanager import ProxyManager
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import gevent
import urllib2
import gzip
import StringIO
import re
import random
import MySQLdb
import datetime

class AccessUrls:

    def __init__(self):
        self.gevent_timeout = 20#seconds
    def requestUrl(self,url,try_idx):
        if proxymgr != None:
            proxy = proxymgr.next_proxy(url).proxy
        headers = {
            'User-Agent': useragents[random.randint(0, len(useragents) - 1)]}
        try_time = 0
        while(try_time < try_idx):
            try:
                with gevent.Timeout(self.gevent_timeout, Exception("gevent-timeout: %d seconds" % self.gevent_timeout)):
                    logging.info("task(%s, try=%s): called", url, try_time)
                    if proxymgr != None:
                        opener = urllib2.build_opener(urllib2.ProxyHandler(
                                {'http': proxy}), urllib2.HTTPHandler(debuglevel=1))
                    else:
                        opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
                    urllib2.install_opener(opener)  # add exception here
                    request = urllib2.Request(url)
                    request.add_header(
                        'User-Agent',
                        useragents[
                            random.randint(
                                0,
                                len(useragents) -
                                1)])
                    request.add_header('connection', 'keep-alive')
                    request.add_header('Accept-Encoding', 'gzip')
                    response = urllib2.urlopen(request)
                    html = response.read()
            except Exception as e:
                if proxymgr != None:
                    proxymgr.feedback(proxy, False)
                logging.error("task(%s, %s) - %s" % (url, try_idx, e))
                try_time += 1
            else:
                if proxymgr != None:
                    proxymgr.feedback(proxy, True)
                if(response.headers.get('content-encoding', None) == 'gzip'):
                    html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()
                #print html
                return html 
        logging.error("task(%s) - Max try time exceed.Abort." % (url))
        return None
    @staticmethod
    def task(self, url, try_idx, extractSearchResults):
        html = self.requestUrl(url,try_idx)
        if html!= None:
            extractSearchResults(html)
    @staticmethod
    def taskGenerator(self,urls,extractSearchResults):
        try:
            assert len(urls) > 0
        except AssertionError:
            logging.error('Fail to get urls,Program Aborted')
            sys.exit()
        else:
            for url in urls:
                yield gtaskpool.Task(AccessUrls.task, [self, url,3,extractSearchResults])

    def gtaskManager(self,urls,extractSearchResults,proxy_flag = 0,ua_flag = 0):
        task_log = None 
        gtaskpool.setlogging(logging.INFO,task_log)
        purl1 = ["http://192.168.120.17:8014/proxy/get_http_proxy_list"]
        uurl1 = "http://192.168.120.17:8014/proxy/get_useragent_list"
        limited_urls = [
            ('^https{0,1}://', 0)
        ]
        global proxymgr

        if proxy_flag == 1:
            proxymgr = ProxyManager(get_http_proxies, limited_urls,
                                {'refresh': True, 'interval': 30 * 60, 'delay': 8 * 60}, *purl1)
        else:
            proxymgr = None
        print proxymgr
        global useragents
        if ua_flag == 1:
            useragents = get_useragents(uurl1)
        else:
            useragents = [None]
        if useragents == []:
            useragents = [None]

        gtaskpool.runtasks(AccessUrls.taskGenerator(self,urls,extractSearchResults))
def extractSearchResults(html):
    '''
    for test
    '''
    print html
if __name__ == "__main__":
    #urls = ['http://www.iie.ac.cn/','http://www.163.com/','http://nelist.iie.ac.cn/']
    urls = list()
    with open('urls_to_access.txt',"rb") as f:
        for line in f:
            urls.append(line.strip('\n'))
    a = AccessUrls()
    a.gtaskManager(urls,extractSearchResults)
