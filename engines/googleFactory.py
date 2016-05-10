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
class GoogleFactory(EngineFactory):
    def __init__(self):
        self.engine_name = "Google"
        self.engine_domain = "https://www.google.de/"
        self.weight = 5
        self.results_num = 100
        self.page_num = 10
    def urlGenerator(self,query):
        urls_list = list()
        try:
            assert self.page_num > 0 and self.results_num > 0
        except AssertionError:
            logging.error(
                'Parameter error,please check the parameters.Program Aborted')
        else:
            urls = list()
            results_per_page = self.results_num/self.page_num
            for p in range(0, self.page_num):
                first = p * results_per_page
               # url = '%ssearch?hl=en&num=%d&start=%s&q=%s&filter=0' % (
               #     self.engine_domain, results_per_page, start, query)
                url = 'https://search.disconnect.me/searchTerms/search?start=nav&option=Web&query='+query+'&ses=Google&location_option=US&nextDDG=%2Fsearch%3Fq%3D%26hl%3Den%26start%3D'+str(first)+'%26sa%3DN&showIcons=false&filterIcons=none&js_enabled=1&source=None'
                urls_list.append(url)
        return urls_list
    def extractSearchResults(self,html):
        print html
        '''
        results = list()
        soup = BeautifulSoup(html)
        div = soup.find('div', id='search')
        if (not isinstance(div, types.NoneType)):
            lis = div.findAll('li', {'class': 'g'})
            if(len(lis) > 0):
                for li in lis:
                    result = SearchResult()
                    h3 = li.find('h3', {'class': 'r'})
                    if(isinstance(h3, types.NoneType)):
                        continue
                    link = h3.find('a')
                    if (isinstance(link, types.NoneType)):
                        continue
                    url = link['href']
                    url = self.extractUrl(self, url)
                    if(cmp(url, '') == 0):
                        continue
                    title = link.renderContents()
                    result.setURL(url)
                    result.setTitle(title)
                    span = li.find('span', {'class': 'st'})
                    if (not isinstance(span, types.NoneType)):
                        content = span.renderContents()
                        result.setContent(content)
                    results.append(result)
        return results
        '''
        search_results = list()
        soup = BeautifulSoup(html)
        try:
            ul = soup.find_all('ul',id='normal-results')
            lis = ul[0].find_all('li')
        except:
            logging_error("fail to extract the page:%s", url)
        else:
            for li in lis:
                search_result = SearchResult()
                search_result.setURL(li.find('a')['href'])
                search_result.setContent(li.find('p').text)
                search_result.setTitle(li.find('a').text)
                if bloom_filter.is_not_contained(search_result.getURL()):
                    bloom_filter.bf_add(search_result.getURL())
                    search_results.append(search_result)
            return search_results

