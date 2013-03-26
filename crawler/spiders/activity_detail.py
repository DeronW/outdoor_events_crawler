from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from crawler.items import ActivityItem
from crawler.db import get_start_urls
from crawler import pipelines

class ChinaWalkingActivitySpider(BaseSpider):

    name = 'cw'
    allowed_domains = ['http://www.chinawalking.net.cn']
    start_urls = get_start_urls('www.chinawalking.net.cn')

    pipeline = set([
        pipelines.DetailFilterPipeline,
        pipelines.DetailSavePipeline,
    ])

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//div[@id="nr_zuo"]/dl/dt/text()').extract()[0]
        data = hxs.select('//div[@id="nr_zuo"]/dl/dd')

        get_text = lambda x: data[x].select('text()').extract()[0] #.encode('utf8')

        item = ActivityItem()
        item['source_site'] = 'http://www.chinawalking.net.cn'
        item['activity_link'] = response.url
        item['subject'] = title
        item['leaderuname'] = get_text(0)
        item['contact'] = get_text(1)
        #item['ways'] = get_text(2)
        #item['activity_strength'] = get_text(3)
        item['destplace'] = get_text(4)
        item['starttimefrom'] = 0 # get_text(5)
        item['starttimeto'] = 1 #get_text(5)
        #item['gather_location'] = get_text(6)
        #item['fee'] = get_text(7)
        #item['people_limit'] = get_text(8)
        #item['expired_time'] = get_text(9)
        #item['activity_type'] = get_text(10)
        #item['commercial_type'] = get_text(11)
        return item

