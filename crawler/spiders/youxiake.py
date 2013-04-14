# -*- encoding:utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from crawler import pipelines
from crawler.items import ListItem, ActivityItem
from crawler.db import get_start_urls

import re
import time

class YouxiakeMainSpider(BaseSpider):
    name = 'y'
    allowed_domains = ['xia.youxiake.com']
    start_urls = ['http://xia.youxiake.com/circle.php?do=circleinfor&pid=11']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        links = hxs.select('//div[@class="viciao"]/a')
        last_page_url = links[-1].select('.//@href').extract()[0]
        r = re.compile('\d+')
        nums = r.findall(last_page_url)
        last_page = int(nums[-1])
        for i in range(1, last_page + 1):
            yield Request('http://xia.youxiake.com/circle.php?do=circleinfor&pid=11&page=%s' % i, callback=self.parse_url)

    def parse_url(self, response):
        hxs = HtmlXPathSelector(response)
        tables = hxs.select('//table[@width="726"]')[2:]
        items = []
        for i in tables:
            item = ListItem()
            item['site'] = 'xia.youxiake.com'
            item['url'] = 'http://xia.youxiake.com/circle.php%s' % i.select('.//td[2]/a/@href').extract()[0]
            items.append(item)
        return items

class YouxiakeActivitySpider(BaseSpider):

    name = 'ya'
    allowed_domains = ['xia.youxiake.com']
    start_urls = get_start_urls('xia.youxiake.com')

    def parse(self, response):

        if response.status == 200:
            self.linkDB.update_info_url(response.url, 'true')
        else:
            self.linkDB.update_info_url(response.url, 'false')

        lvyeItem = LvyeItem()

        item = YouxiakeItem()
        p = re.compile('[0-9]+') 
        x = HtmlXPathSelector(response)
        #item['url'] = url
        lvyeItem['activity_link'] = response.url

        lvyeItem['imgurl'] = x.select("//div[@id='actpic']/img/@src").extract()[0]

        lvyeItem['subject'] = x.select("//span[@id='rtitle']/text()").extract()[0]

        lvyeItem['activity_status'] = x.select("//span[@class='yellowfont']/text()").extract()[0].strip(u'\xa0')

        atype = x.select("/html/body/table[4]/tr/td/table[1]/tr/td/table[2]/tr/td[1]/table[1]/tr[2]/td[2]/table/tr[1]/td[2]/a/text()").extract()[0]
        lvyeItem['activitytype'] = atype.strip(u'\xa0')

        activity_time = x.select("/html/body/table[4]/tr/td/table[1]/tr/td/table[2]/tr/td[1]/table[1]/tr[2]/td[2]/table/tr[2]/td[2]/text()").extract()[0]
        times = activity_time.split('~')
        former = times[0].strip(u'\xa0')
        start_time = time.mktime(time.strptime(former,'%Y-%m-%d'))
        lvyeItem['starttimefrom'] = int(start_time)
        end_time = start_time
        if len(times) > 1:
            end_time = time.mktime(time.strptime(times[1],'%Y-%m-%d'))
        lvyeItem['starttimeto'] = int(end_time)

        destination = x.select("/html/body/table[4]/tr/td/table[1]/tr/td/table[2]/tr/td[1]/table[1]/tr[2]/td[2]/table/tr[3]/td[2]/a[last()]/text()").extract()[0]
        lvyeItem['destplace'] = destination

        venue = x.select("/html/body/table[4]/tr/td/table[1]/tr/td/table[2]/tr/td[1]/table[1]/tr[2]/td[2]/table/tr[3]/td[4]/a[last()]/text()").extract()[0]
        lvyeItem['depart_place'] = venue

        bnum = x.select("/html/body/table[4]/tr/td/table[1]/tr/td/table[2]/tr/td[1]/table[1]/tr[2]/td[2]/table/tr[5]/td[2]/text()").extract()[0]
        lvyeItem['views_number'] = bnum.strip(u'\xa0')
            
        expense = '0' 
        try:
            expense = x.select("/html/body/table[4]/tr/td/table[1]/tr/td/table[2]/tr/td[1]/table[1]/tr[2]/td[2]/table/tr[4]/td[2]/span[1]/text()").extract()[0]
            expense = p.findall(expense)[0]
            lvyeItem['price'] = int(expense)
        except:
            log.msg('the activity the price is null:' + response.url, log.INFO)

        applynum = '0'
        p1 = re.compile(u'已申请报名 ([0-9]+) 人'.encode('gbk'))
        tem = p1.search(response.body)
        if tem:
             applynum = tem.group(1)
        lvyeItem['applynumber'] = int(applynum)

        unconfirm_num = '0'
        p2 = re.compile(u'未审核\(([0-9]+)\)人'.encode('gbk'))
        tem = p2.search(response.body)
        if tem:
            unconfirm_num = tem.group(1)
        lvyeItem['remainnumber'] = unconfirm_num    
        lvyeItem['source_site'] = u'游侠客'
        return lvyeItem
