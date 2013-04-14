# -*- encoding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from crawler import pipelines
from crawler.items import ListItem, ActivityItem
from crawler.db import get_start_urls

import re
import time
import sys


class Www8264MainSpider(BaseSpider):
    name = '8'
    allowed_domains = ['www.8264.com', 'u.8264.com']
    start_urls = ["http://u.8264.com/home-space-do-activity-view-all-order-hot-date-default-class.html"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        tpage = int(hxs.select('//*[@id="wp"]/div[5]/div[3]/em/div/div/a[10]/text()').extract()[0].replace('... ',''))  
        for i in range(1, tpage+1):
            yield Request('http://u.8264.com/home-space-do-activity-view-all-order-hot-date-default-page-%s.html' % i, callback=self.parse_url)

    def parse_url(self, response):
        hxs = HtmlXPathSelector(response)
        links = hxs.select('//*[@id="threadlist"]//th[@class="new"]/a/@href').extract()
        items = []
        for i in links:
            item = ListItem()
            item['site'] = 'www.8264.com'
            item['url'] = i
            items.append(item)
        return items

class Www8264ActivitySpider(BaseSpider):
    name = '8a'
    allowed_domains = ['www.8264.com', 'u.8264.com']
    start_urls = get_start_urls('www.8264.com')

    def parse(self, response):
        item = W8264() 
        lvyeItem = LvyeItem()
        hxs = HtmlXPathSelector(response)

        try:
            error = hxs.select('//*[@id="postlist"]/div[1]/table/tr[1]/td[2]/div[3]/div[3]/div/em').extract()[0]
            print 'the activity is deleted :' + response.url
            log.msg('the activity is deleted :'  + response.url, log.WARNING)
            return
        except:
            pass

        try:
            lvyeItem['subject'] = hxs.select('//*[@id="thread_subject"]/text()').extract()[0]
        except:
            print 'no subject for activity :' + response.url
            log.msg('no subject for activity :'  + response.url, log.WARNING)
            return

        lvyeItem['activity_link'] = response.url
        lvyeItem['imgurl'] = '';

        try:
            lvyeItem['imgurl'] = hxs.select('//*[@id="postlist"]/div[1]/table/tr[1]/td[2]/div[3]/div[3]/div[1]/div[1]/div[1]/a/img/@src').extract()[0]
        except:
            log.msg('the activity no photo :' + response.url, log.INFO)

        dls = hxs.select('//*[@id="postlist"]/div[1]/table/tr[1]/td[2]/div[3]/div[3]/div[1]/div[1]/div[2]//dt')
        dds = hxs.select('//*[@id="ct"]/div[2]/div[1]/table/tr[1]/td[2]/div[3]/div[3]/div[1]/div[1]/div[2]//dd')


        hdtime = ''
        count = 0
        remainnumber = ""
        expiration = ""
        for dl in dls:
            dltexts = dl.select('text()').extract()
            if len(dltexts) > 0:
                if dltexts[0].count(u'活动类型'):
                    lvyeItem['activitytype'] =  dds[count].select('strong/text()').extract()[0]
                if dltexts[0].count(u'开始时间'):
                    hdtime =  dds[count].select('text()').extract()[0]
                if dltexts[0].count(u'活动地点'):
                    lvyeItem['destplace'] = dds[count].select('text()').extract()[0]
                if dltexts[0].count(u'已报名人数'):
                    lvyeItem['applynumber'] = dds[count].select('em/text()').extract()[0]
                if dltexts[0].count(u'剩余名额'):
                    remainnumber =  dds[count].select('text()').extract()[0]
                    ptemp = re.compile('[0-9]+')
                    remainnumber = ptemp.findall(remainnumber)[0]
                    lvyeItem['remainnumber'] = remainnumber 
                if dltexts[0].count(u'报名截止'):
                    expiration =  dds[count].select('text()').extract()[0]
                    expiration = time.mktime(time.strptime(expiration, '%Y-%m-%d %H:%M'))
                    lvyeItem['expiration'] = expiration 
                if dltexts[0].count(u'每人花销'):
                    price =  dds[count].select('text()').extract()[0]
                    ptemp = re.compile('[0-9]+') 
                    tmp = ptemp.search(price)
                    if tmp:
                        lvyeItem['price'] = tmp.group(0) 
            count = count+1

        if hdtime.count(u'前'):
            print 'Activities have already begun :'+ response.url
            log.msg('Activities have already begun :'+ response.url, log.WARNING)
            return

        p = re.compile('[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+')
        times = p.findall(hdtime)
        starttimefrom = 0 
        starttimeto = 0 

        if len(times) < 1:
            return
        try:
            if len(times) <= 1:
                lvyeItem['starttimefrom'] = starttimefrom = time.mktime(time.strptime(times[0], '%Y-%m-%d %H:%M'))
            else:
                lvyeItem['starttimefrom'] = starttimefrom = time.mktime(time.strptime(times[0], '%Y-%m-%d %H:%M'))
                lvyeItem['starttimeto'] = starttimeto = time.mktime(time.strptime(times[1], '%Y-%m-%d %H:%M'))
        except:
            print 'the date formate is error :'+ response.url
            log.msg('The Activity date formate is error :'+ response.url, log.ERROR)
            return

        lvyeItem['source_site'] = u'户外资料网'  
                
        return lvyeItem

    def err_info(self, response):
        self.linkDB.update_info_url(response.url, 'false')


