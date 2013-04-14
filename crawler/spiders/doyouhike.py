from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from crawler import pipelines
from crawler.items import ListItem, ActivityItem
from crawler.db import get_start_urls

import json
import time

class DoyouhikeSpider(BaseSpider):

    name = 'd'
    allowed_domains = ['www.doyouhike.net']
    start_urls = ["http://www.doyouhike.net/event/s?keywords=&page=1"]

    pipeline = set([
        pipelines.ListSavePipeline,
    ])

    def parse(self, response):
        data = json.loads(response.body)
        tpage = int(data['tpage'])
        items = []
        for i in range(1, tpage+1):
            yield Request('http://www.doyouhike.net/event/s?keywords=&page=%s' % i, callback=self.parse_url) 

    def parse_url(self, response):
        data = json.loads(response.body)
        activities = data['result']
        for i in activities:
            item = ListItem()
            item['url'] = 'http://www.doyouhike.net%s' % i['url']
            item['site'] = 'www.doyouhike.net'
        return item

class DoyouhikeActivitySpider(BaseSpider):
    name = 'dm'
    allowed_domains = ['www.doyouhike.net']
    start_urls = ["http://www.doyouhike.net/event/s?keywords=&page=1"]

    pipeline = set([
        pipelines.DetailFilterPipeline,
        pipelines.DetailSavePipeline,
    ])

    def parse(self, response):
        data = json.loads(response.body)
        tpage = int(data['tpage'])
        items = []
        for i in range(1, tpage+1):
            yield Request('http://www.doyouhike.net/event/s?keywords=&page=%s' % i, callback=self.parse_url) 

    def parse_url(self, response):
        data = json.loads(response.body)
        activities = data['result']
        for i in activities:
            if i['EventState'] == 'finish':
                continue
            item = ActivityItem()
            item['subject'] =  i['EventTitle']
            item['leaderuname'] =  i['UserName']
            item['activity_detail'] =  i['EventDesc']
            item['SCHlen'] =  i['Days']
            item['activity_status'] = i['EventState']
            item['max_apply'] =  i['MemberLimit']
            item['applynumber'] = i['MemberNum']
            item['destplace'] = i['DestName']
            item['source_site'] = 'www.doyouhike.net' 
            item['starttimefrom'] = time.mktime(time.strptime(i['EventDate'], '%Y-%m-%d')) + int(i['Days']) * 24 * 60 * 60
            yield Request('http://www.doyouhike.net%s' %  i['url'], meta={'item': item}, callback=self.parseItem) 

    def parseItem(self,response):
        item = response.meta['item']

        hxs = HtmlXPathSelector(response)
        cityname = hxs.select('//*[@id="topic_post_list"]/div/table/tr[2]/td[2]/div[1]/ul/li[3]/text()').extract()  
        if cityname:
            name = cityname[0].replace('\t','').replace('\r\n','').replace(' ','')
            item['depart_place'] = name
        return item

