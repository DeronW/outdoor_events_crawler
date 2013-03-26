from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from crawler.items import ListItem
from crawler import pipelines

class ChinaWalkingMainSpider(BaseSpider):
    name = 'c'
    allowed_domains = ['http://www.chinawalking.net.cn']
    #start_urls = ['http://www.chinawalking.net.cn/newsite/huodong.php?PageNo=%s' % i for i in range(35)]
    start_urls = ['http://www.chinawalking.net.cn/newsite/huodong.php?PageNo=%s' % i for i in range(2)]

    pipeline = set([
        pipelines.ListSavePipeline,
    ])

    def parse(self, response):
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
