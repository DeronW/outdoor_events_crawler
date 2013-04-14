from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from crawler import pipelines
from crawler.items import ListItem, ActivityItem
from crawler.db import get_start_urls

import re

class SanfoMainSpider(BaseSpider):

    name = 's'
    allowed_domains = ['www.sanfo.com']
    start_urls = ['http://www.sanfo.com/travel/index.asp?citycode=BJ&page=1']

    pipeline = set([
        pipelines.ListSavePipeline,
    ])

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        href = hxs.select('//*[@id="page"]/a[8]/@href')
        
        r = re.compile('\d+')
        result = r.findall(href)
        num = int(result[-1])

class SanfoActivitySpider(BaseSpider):
    
    name = 'la'
    allowed_domains = ['www.lvzhou.info']
    start_urls = get_start_urls('www.lvzhou.info')

    pipeline = set([
        pipelines.DetailFilterPipeline,
        pipelines.DetailSavePipeline,
    ])

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        item = ActivityItem()
        return item

