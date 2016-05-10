#!/usr/bin/env python
# encoding: utf-8
from enginesFactory import EngineFactory
from bs4 import BeautifulSoup
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import random
import types
import os
from searchResult import SearchResult
class SogouFactory(EngineFactory):
    def __init__(self):
        self.engine_name = "Sogou"
        self.engine_domain = "http://www.sogou.com/"
        self.weight = 5
        self.results_num = 100
        self.page_num = 1
    def urlGenerator(self,query):
        urls_list = list()
        try:
            assert self.page_num > 0 and self.results_num > 0
        except AssertionError:
            logging.error(
                'Parameter error,please check the parameters.Program Aborted')
        else:
            urls = list()
            for p in range(1, self.page_num+1):
                url = self.engine_domain+"web?query="+query+"&page="+str(p)+"&ie=utf8"
                urls_list.append(url)
        return urls_list
    def extractSearchResults(self,html):
        #print html
        search_results = list()
        soup = BeautifulSoup(html)
        try:
            ul = soup.find_all('div',class_='results')
            lis = ul[0].children

        except:
            logging_error("fail to extract the page:%s", url)
        else:
            for li in lis:
                search_result = SearchResult()
                try:
                    search_result.setURL(li.find('a')['href'])
                except:
                    search_result.setURL("")
                try:
                    search_result.setContent(li.find('p').text)
                except:
                    search_result.setContent("")
                try:
                    search_result.setTitle(li.find('a').text)
                except:
                    search_result.setTitle("")
                if search_result.getURL() != "":
                    search_result.printIt()
                    search_results.append(search_result)
            return search_results
