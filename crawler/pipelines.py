# -*- encoding: utf-8 -*-

from functools import wraps
from scrapy import log

from crawler.db import ListDB, DetailDB
from crawler.util import format_time

DETAIL_FIELD = {
    'imgurl': '',
    'SCHtype': '',
    'SCHlen': 0,
    'daytype': '',
    'date_dimension':'',
    'max_apply': 0,
    'expiration': 0,
    'starttimefrom': 0,
    'starttimeto': 0,
    'destplace': '',
    'activitytype': '',
    'leaderuname': '',
    'leaderurl': '',
    'hard_level': '',
    'price': 0,
    'event_property': 'AA',
    'leader_score': 0,
    'subject':'',
    'depart_place': '',
    'redbull': 0,
    'lottery': 0,
    'paytype': '',
    'holiday': '',
    'leader_grade': 'D',
    'goodrate': 0.0,
    'allmarks': 0,
    'leader_medal': '',
    'leader_medal_name': '',
    'applynumber': 0,
    'remainnumber': 0,
    'activity_score': 0,
    'activity_status': 'applying',
    'activity_detail': '',
    'route': '',
    'trip_mode': '',
    'views_number': 0,
    'follow_number': 0,
    'public_degree': 'public',
    'activity_link': '',
    'source_site': '',
    'contact': '',
}

def check_spider_pipeline(process_item_method):
    """ check if current item source is the spider that define pipelines contain this pipeline """
    @wraps(process_item_method)
    def wrapper(self, item, spider):
        try:
            if self.__class__ in spider.pipeline:
                return process_item_method(self, item, spider)
        except AttributeError:
            pass
        return item
    return wrapper

class ListSavePipeline(object):

    def __init__(self):
        self.listdb = ListDB()

    @check_spider_pipeline
    def process_item(self, item, spider):
        list_id = self.listdb.get_list_id(item['url'])
        if list_id:
            self.listdb.update_url(list_id=list_id, url=item['url'], site=item['site'])
        else:
            self.listdb.add_url(url=item['url'], site=item['site'])
        return item

class DetailFilterPipeline(object):

    @check_spider_pipeline
    def process_item(self, item, spider):
        tfrom = item.get('starttimefrom', 0)
        tto = item.get('starttimeto', 0)
        item.update(format_time(tfrom, tto))
        return item

class DetailSavePipeline(object):

    def __init__(self):
        self.db = DetailDB()

    @check_spider_pipeline
    def process_item(self, item, spider):
        d = DETAIL_FIELD.copy()
        d.update(item)
        columns = ''
        values = ''
        for i in d:
            columns += ',' + i
            if isinstance(d[i], int) or isinstance(d[i], float):
                values += ',{%s}' % i
            else:
                values += ',"{%s}"' % i
        statement = u'INSERT INTO activity_search (%s) VALUES (%s)' % (columns[1:], values[1:])
        statement = statement.format(imgurl=d['imgurl'], SCHtype=d['SCHtype'], SCHlen=d['SCHlen'], daytype=d['daytype'], date_dimension=d['date_dimension'], max_apply=d['max_apply'], expiration=d['expiration'], starttimefrom=d['starttimefrom'], starttimeto=d['starttimeto'], destplace=d['destplace'], activitytype=d['activitytype'], leaderuname=d['leaderuname'], leaderurl=d['leaderurl'], hard_level=d['hard_level'], price=d['price'], event_property=d['event_property'], leader_score=d['leader_score'], subject=d['subject'], depart_place=d['depart_place'], redbull=d['redbull'], lottery=d['lottery'], paytype=d['paytype'], holiday=d['holiday'], leader_grade=d['leader_grade'], goodrate=d['goodrate'], allmarks=d['allmarks'], leader_medal=d['leader_medal'], leader_medal_name=d['leader_medal_name'], applynumber=d['applynumber'], remainnumber=d['remainnumber'], activity_score=d['activity_score'], activity_status=d['activity_status'], activity_detail=d['activity_detail'], route=d['route'], trip_mode=d['trip_mode'], views_number=d['views_number'], follow_number=d['follow_number'], public_degree=d['public_degree'], activity_link=d['activity_link'], source_site=d['source_site'], contact=d['contact'])
        self.db.save(statement)
        return item

