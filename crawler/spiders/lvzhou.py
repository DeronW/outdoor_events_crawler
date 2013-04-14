from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from crawler import pipelines
from crawler.items import ListItem, ActivityItem
from crawler.db import get_start_urls

import datetime
import re

class LvzhouMainSpider(BaseSpider):

    name = 'l'
    allowed_domains = ['www.lvzhou.info']
    start_urls = ['%s%s' % ('http://www.lvzhou.info/home.php?mod=space&do=activity&view=all&order=dateline&page=', i) for i in range(5)]

    pipeline = set([
        pipelines.ListSavePipeline,
    ])

    def __init__(self):
        self.today = datetime.datetime.today().date().isoformat()

    def match_date(self, s):
        r = re.compile('(\d+)')
        return '-'.join(r.findall(s))

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        tables = hxs.select('//*[@class="bm bw0"]/table')
        urls = []

        for t in tables:
            text = t.select('.//h3[@class="cl"]/text()').extract()
            if self.today > self.match_date(''.join(text)):
                break
            links = t.select('.//h4/a/@href').extract()
            urls.extend(links)

        items = []
        for url in urls:
            item = ListItem()
            item['site'] = 'www.lvzhou.info'
            item['url'] = url
            items.append(item)

        return items

class LvzhouActivitySpider(BaseSpider):
    
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

