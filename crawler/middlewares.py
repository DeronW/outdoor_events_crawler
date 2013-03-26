from scrapy import log
from crawler.db import MySQLCursor

class RepeatUrlMiddleware(object):

    def __init__(self):
        self.db = MySQLCursor()

    def process_spider_input(self, response, spider):
        log.msg('spider : %s , url : %s' % (spider.name, response.url))
        return None

    def process_start_requests(self, start_requests, spider):
        requests = []
        for r in start_requests:
            if not self.db.is_crawled_url(r.url):
                self.db.add_url(r.url)
                requests.append(r)
        return start_requests

