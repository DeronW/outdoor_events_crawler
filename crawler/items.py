# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ListItem(Item):
    url = Field()
    site = Field()

class ActivityItem(Item):
    imgurl = Field()
    SCHtype = Field()
    SCHlen = Field()
    daytype = Field()
    date_dimension = Field()
    max_apply = Field()
    expiration = Field()
    starttimefrom = Field()
    starttimeto = Field()
    destplace = Field()
    activitytype = Field()
    leaderuname = Field()
    leaderurl = Field()
    hard_level = Field()
    price = Field()
    event_property = Field()
    leader_score = Field()
    subject = Field()
    depart_place = Field()
    redbull = Field()
    lottery = Field()
    paytype = Field()
    holiday = Field()
    leader_grade = Field()
    goodrate = Field()
    allmarks = Field()
    leader_medal = Field()
    leader_medal_name = Field()
    applynumber = Field()
    remainnumber = Field()
    activity_score = Field()
    activity_status = Field()
    activity_detail = Field()
    route = Field()
    trip_mode = Field()
    views_number = Field()
    follow_number = Field()
    public_degree = Field()
    activity_link = Field()
    source_site = Field()
    contact = Field()

