from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from crawler import pipelines
from crawler.items import ListItem, ActivityItem
from crawler.db import get_start_urls

class ChinaWalkingMainSpider(BaseSpider):
    name = 'c'
    allowed_domains = ['www.chinawalking.net.cn']
    start_urls = ['http://www.chinawalking.net.cn/newsite/huodong.php?PageNo=1']

    pipeline = set([
        pipelines.ListSavePipeline,
    ])

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        links = hxs.select('//p[@class="yema"]/a/@href')
        nums = links.re('\d+')
        pages = int(nums[-1])
        for i in range(1, pages):
            yield Request('http://www.chinawalking.net.cn/newsite/huodong.php?PageNo=%s' % i, callback=self.parse_detail_url)

    def parse_detail_url(self, response):
        hxs = HtmlXPathSelector(response)
        links = hxs.select('//li[@class="mingzi"]/a')
        
        items = []
        for i in links:
            title = i.select('text()').extract()[0]
            link = i.select('@href').extract()[0]
            item = ListItem()
            item['url'] = '%s/%s' % ('http://www.chinawalking.net.cn/newsite', link)
            item['site'] = 'www.chinawalking.net.cn'
            items.append(item)
        return items

class ChinaWalkingActivitySpider(BaseSpider):

    name = 'cw'
    allowed_domains = ['www.chinawalking.net.cn']
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

