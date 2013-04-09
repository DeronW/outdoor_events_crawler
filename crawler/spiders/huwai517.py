from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from crawler import pipelines
from crawler.items import ListItem, ActivityItem
from crawler.db import get_start_urls

import datetime
import urllib2

def get_url_range():
    num = 0
    urls = []
    base_url = 'http://www.517huwai.com/Activity/index/?beginDate=%s' % datetime.datetime.today().date().isoformat()
    while True:
        num += 1
        url = '%s&p=%s' % (base_url, num)
        print url
        r = urllib2.urlopen(url)
        if len(r.read()) < 100 or num > 50:
            break;
        else:
            urls.append(url)
    return urls

class Huwai517Spider(BaseSpider):
    name = 'h'
    allowed_domains = ['www.517huwai.com']
    start_urls = get_url_range()

    pipeline = set([
        pipelines.ListSavePipeline,
    ])

    def parse(self, response):
        print response.url

