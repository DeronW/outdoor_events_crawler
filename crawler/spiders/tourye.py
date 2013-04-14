from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from crawler import pipelines
from crawler.items import ListItem, ActivityItem
from crawler.db import get_start_urls

import re

class TouryeMainSpider(BaseSpider):
    name = 't'
    allowed_domains = ['www.tourye.com', 'u.tourye.com/']
    start_urls = ['http://u.tourye.com/space.php?do=event&view=all&type=signing&classid=1']
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        last_page_url = hxs.select('//*[@class="page"]/a[@class="last"]/@href').extract()[0]
        r = re.compile('\d+')
        nums = r.findall(last_page_url)
        last_page = int(nums[-1])
        for i in range(1, last_page + 1):
            yield Request('http://u.tourye.com/space.php?uid=0&do=event&view=all&type=signing&classid=1&page=%s' % i, callback=self.parse_url)

    def parse_url(self, response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.select('//*[@class="event_icon"]/a/@href').extract()
        items = []
        for i in urls:
            item = ListItem()
            item['site'] = 'www.tourye.com'
            item['url'] = 'u.tourye.com/%s' % i
            items.append(item)
        return items

class TroryeActivitySpider(BaseSpider):

    name = 'ta'
    allowed_domains = ['u.tourye.com/']
    start_urls = get_start_urls('www.tourye.com')

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//*[@id="mainarea"]/h2/a[2]/text()').extract()[0]
        picurl = hxs.select('//*[@id="content"]/div[1]/div/div[1]/a/img/@src').extract()[0]
        picurl = 'http://u.tourye.com/'+picurl
        leader_name = hxs.select('//*[@id="content"]/div[1]/div/div[2]/dl/dd/a/text()').extract()[0]
        leader_url = hxs.select('//*[@id="content"]/div[1]/div/div[2]/dl/dd/a/@href').extract()[0]
        leader_url = 'http://u.tourye.com/'+leader_url
        info = hxs.select('//*[@id="content"]/div[1]/div/div[2]/dl/dd')
        
        get_info = lambda x: info[x].select('text()').extract()[0] 
        try:
            remainnumber = get_info(6).split()[2]
        except:
            remainnumber = 0

        eventnumber  = get_info(6).split()[0]
        
        try:
            eventnumber = int(eventnumber)
        except:
            eventnumber = 9999
        item = TaoyeItem()
        item['activity_link'] = response.url
        item['imgurl'] = picurl
        item['subject'] = title
        item['leaderuname'] = leader_name
        item['leaderurl'] = leader_url
        item['activitytype'] = get_info(1)
        item['destplace'] = get_info(2).split()[-1]
        item['starttimefrom'] = time.mktime(time.strptime(get_info(3).split('-')[0].strip(), '%Y.%m.%d %H:%M'))
        item['starttimeto'] = time.mktime(time.strptime(get_info(3).split('-')[-1].strip(), '%Y.%m.%d %H:%M'))
        item['contact'] = hxs.select('//*[@id="content"]/div[1]/div/div[2]/dl/dd[6]/strong/text()').extract()[0]
        item['max_apply'] = eventnumber
        item['remainnumber'] = remainnumber
        item['views_number'] = hxs.select('//*[@id="content"]/div[1]/div/div[2]/ul[1]/li[1]/text()').extract()[0].split()[0]
        item['applynumber'] = hxs.select('//*[@id="content"]/div[1]/div/div[2]/ul[1]/li[2]/text()').extract()[0].split()[0]
        item['follow_number'] = hxs.select('//*[@id="content"]/div[1]/div/div[2]/ul[1]/li[3]/text()').extract()[0].split()[0]
        # item['event_detail'] = hxs.select('//*[@id="content"]/div[2]/div').extract()[0]
        return item

