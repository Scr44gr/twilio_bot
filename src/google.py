# -*- coding: utf-8 -*-
from robobrowser import RoboBrowser
from newsapi import NewsApiClient as search_new
import re
import random
import time
__author__ = "Scr44gr"

class news:

    def run(self):
        self.random_agents()
        self.open_session()
        self._news_()

    def open_session(self):

        try:
            self.session = RoboBrowser(user_agent=self.user_agents, history=True, parser='lxml')
            self.session.open(self.url)
        except:
            time.sleep(5)
            self.open_session()

    def random_agents(self):

        self.cache = []
        self.repeat = []
        list_agents = ['Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36','Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16','Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14','Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14','Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201']
        self.user_agents = random.choice(list_agents)
        self.url = "https://news.google.com"


    def _news_(self):
        """this function its for search the news in the DOM(news.google.com), using the re library"""
        html = str(self.session.parsed())

        for u in re.findall(r'<h3>(.*)</h3>', html, re.MULTILINE): #I use re.findall and re.MULTILINE to search in the tag <h3>

            try:
                new = re.search(r'<span>(.*)</span>', u, re.MULTILINE).group(1)#After, repeat what I do before, but in this case is for search the news in the tag <span>

                if not re.search(r'</span>(.*)', new):
                    self.cache.append(new)
            except:
                pass

        self.cache = list(set(self.cache))

    def get_news(self):

        if self.cache == []:
            print("[*] cleaned cache  ")
            time.sleep(5)
            print("[*] restart news_function")
            return "RESTART"
        else:
            news = random.choice(self.cache)

            if not news in self.repeat and news is not None:

                self.repeat.append(news)
                self.cache.remove(news)
                return news + '\n source: Google News'

            else:
                time.sleep(0.2)
                print("[*] --- update --- ")
                self.get_news()


class search_news:

    def __init__(self):
        self.news = search_new(api_key='')

    def search(self, q=''):
        a = self.news.get_everything(q=q)
        return  a['articles'][0]['title'] + '\n' + a['articles'][0]['description'] +'\n' + a['articles'][0]['url']
