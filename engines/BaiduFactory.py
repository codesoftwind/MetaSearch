'''
Created on 2016-5-11

@author: Administrator
'''
# encoding: utf-8
import requests
import logging
from bs4 import BeautifulSoup

class BaiduFactory:
    def __init__(self):
        self.engine_name="Baidu"
        self.engine_domain="http://www.baidu.com/"
        self.weight=5
        self.results_num=100
        self.page_num=10
    
    def urlGenerator(self,query):
        url_list=list()
        try:
            assert self.page_num > 0 and self.results_num > 0
        except AssertionError:
            logging.error(
                'Parameter error,please check the parameters.Program Aborted')
        else:
            results_per_page= self.results_num/self.page_num
            for i in range(self.page_num):
                url='http://www.baidu.com/s?wd='+query+'&rn='+results_per_page+'&pn='+results_per_page*i+'&ie=utf8'
                url_list.append(url)
            return url_list
    def extractSearchResults(self,html):
        search_results=list()
        soup=BeautifulSoup(html)
        result=list()
        try:
            result=soup.find_all('div',class_="c-container")
        except:
            logging.error("fail to extract the page:%s", '')
        else:
            for li in result:
                 search_result= SearchResult()
                 try:
                     search_result.setURL(li.find('h3',class_="t").a.get('href'))
                 except:
                     search_result.setURL('')
                    
                 try:
                     search_result.setContent(li.find('div',class_="c-abstract").text)
                 except:
                     search_result.setContent('')
                 
                 try:
                     search_result.setTitle(li.find('h3',class_="t").a.text)
                 except:
                     search_result.setTitle('')
                 if(search_result.getURL()!=''):
                     search_results.append(search_result)
            return search_results     
                    
 
