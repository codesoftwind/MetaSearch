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
    @staticmethod
    def task(self, url, try_idx):
        proxy = proxymgr.next_proxy(url).proxy
        proxies = {'http': proxy, 'https': proxy}
        headers = {
            'User-Agent': useragents[random.randint(0, len(useragents) - 1)]}
        try_time = 0
        while(try_time < try_idx):
            try:
                with gevent.Timeout(self.gevent_timeout, Exception("gevent-timeout: %d seconds" % self.gevent_timeout)):
                    logging.info("task(%s, try=%s): called", url, try_time)
                    opener = urllib2.build_opener(urllib2.ProxyHandler(
                        {'http': proxy}), urllib2.HTTPHandler(debuglevel=1))
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
                proxymgr.feedback(proxy, False)
                logging.error("task(%s, %s) - %s" % (url, try_idx, e))
                try_time += 1
            else:
                proxymgr.feedback(proxy, True)
                if(response.headers.get('content-encoding', None) == 'gzip'):
                    html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()
                print html
                return True 
        logging.error("task(%s) - Max try time exceed.Abort." % (url))
        return False
    @staticmethod
    def task_generator(self,urls):
        try:
            assert len(urls) > 0
        except AssertionError:
            logging.error('Fail to get urls,Program Aborted')
            sys.exit()
        else:
            for url in urls:
                yield gtaskpool.Task(AccessUrls.task, [self, url,3])

    def gtaskmanager(self,urls):
        task_log = None 
        gtaskpool.setlogging(logging.INFO,task_log)
        purl1 = ["http://192.168.120.17:8014/proxy/get_http_proxy_list"]
        uurl1 = "http://192.168.120.17:8014/proxy/get_useragent_list"
        limited_urls = [
            ('^https{0,1}://', 0)
        ]
        global proxymgr

        proxymgr = ProxyManager(get_http_proxies, limited_urls,
                                {'refresh': True, 'interval': 30 * 60, 'delay': 8 * 60}, *purl1)
        global useragents
        useragents = get_useragents(uurl1)

        if useragents == []:
            useragents = [None]

        gtaskpool.runtasks(AccessUrls.task_generator(self,urls))
if __name__ == "__main__":
    urls = ['','']
    a = AccessUrls()
    a.gtaskmanager(urls)
