#-*- coding: utf-8 -*-

from datetime import datetime 
import datetime
import time

ACTIVITYTYPE= (u'登山', u'夜爬', u'徒步', u'露营', u'骑行', u'骑马', u'自驾', u'滑雪', u'跑步', u'攀岩', u'垂钓', u'漂流', u'划船', u'冲浪', u'潜水', u'滑翔', u'轮滑', u'滑板', u'航海', u'聚会')

SCHTYPE = {
        ('sat', '1'): u'周六单日',
        ('sat', '2'): u'周末2天',
        ('sun', '1'): u'周日单日',
        ('work', '1'): u'1日',
        ('work', '2'): u'2日',
        ('long', '3'): u'3日',
        ('long', '4'): u'4日',
        ('long', '5'): u'5日',
        ('long', '6'): u'6日',
        ('long', '7-9'): u'7-9日',
        ('long', 'gt9'): u'9日以上',
        }

# param starttimefrom, starttimeto
# return {} and keys: SCHtype, SCHlen, holiday, daytype, date_dimension
def format_time(tfrom, tto):
    arr = (
            ('2012-12-31', '2013-01-01', u'元旦'),
            ('2013-02-09', '2013-02-15', u'春节'),
            ('2013-04-04', '2013-04-06', u'清明'),
            ('2013-04-29', '2013-05-01', u'五一'),
            ('2013-06-10', '2013-06-12', u'端午'),
            ('2013-09-19', '2013-09-21', u'中秋'),
            ('2013-10-01', '2013-10-07', u'十一')
          )
    data = {}
    data['SCHtype'] = 'work'
    data['daytype'] = 'work'
    format = '%Y-%m-%d'
    for start, end, holiday in arr:
        s = int(time.mktime(datetime.strptime(start, format).timetuple()))
        e = int(time.mktime(datetime.strptime(end, format).timetuple()))
        if s <= tfrom < e:
            data['holiday'] = holiday
        else:
            data['holiday'] = ''

    v = datetime.fromtimestamp(float(tfrom)).weekday()
    if v==5:
        data['SCHtype'] = 'sat'
        data['daytype'] = 'weekend'
    elif v==6:
        data['SCHtype'] = 'sun'
        data['daytype'] = 'weekend'
    f = int(time.mktime(datetime.fromtimestamp(tfrom).timetuple()))
    t = int(time.mktime(datetime.fromtimestamp(tto).timetuple()))
    data['SCHlen'] = (t - f) / (60 * 60 * 24) + 1
    datetype = data['SCHtype']
    datelen = str(data['SCHlen'])
    if data['SCHlen'] > 2:
        datetype = 'long'
        daytype = 'long'
        if 7 <= data['SCHlen'] <= 9:
            datelen = '7-9'
        elif data['SCHlen'] > 9:
            datelen = 'gt9'
    data['date_dimension'] = SCHTYPE.get((datetype, datelen), '')
    return data

def today_str():
    return datetime.datetime.today().date().isoformat()
