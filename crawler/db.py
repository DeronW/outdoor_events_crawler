import datetime
import MySQLdb.cursors
from scrapy import log
from scrapy.conf import settings
from twisted.enterprise import adbapi

DB_HOST = settings.get('DB_HOST')
DB_PORT = settings.get('DB_PORT')
DB_USERNAME = settings.get('DB_USERNAME')
DB_PASSWORD = settings.get('DB_PASSWORD')
DB_DBNAME = settings.get('DB_DBNAME')
DB_CHARSET = settings.get('DB_CHARSET')

def get_dbpool(host=DB_HOST, user=DB_USERNAME, passwd=DB_PASSWORD, db=DB_DBNAME, charset=DB_CHARSET):
    return adbapi.ConnectionPool('MySQLdb', host=host, user=user, passwd=passwd, db=db, cursorclass=MySQLdb.cursors.DictCursor, charset=charset) 

def get_cursor(host=DB_HOST, port=DB_PORT, user=DB_USERNAME, passwd=DB_PASSWORD, db=DB_DBNAME, charset=DB_CHARSET):
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset=charset)
    return conn.cursor()

def get_start_urls(site):
    cursor = get_cursor()
    cursor.execute('SELECT * from detail_url WHERE site="%s"' % site)
    result = cursor.fetchall()
    urls = []
    for i in result:
        urls.append(i[1])
    cursor.close()
    return urls

class ListDB(object):

    def __init__(self):
        self.dbpool = get_dbpool()
        self.cursor = get_cursor()

    def close(self):
        self.dbpool.close()
        self.cursor.close()

    def get_list_id(self, url):
        self.cursor.execute('SELECT id FROM detail_url WHERE url="%s" LIMIT 1' % url)
        list_id = self.cursor.fetchone()
        return list_id[0] if list_id else None

    def add_url(self, url, site):
        statement = 'INSERT INTO detail_url (url, site) VALUES ("{url}", "{site}")'.format(url=url, site=site)
        self.dbpool.runOperation(statement)

    def update_url(self, list_id, url, site):
        statement = 'UPDATE detail_url SET site="{site}" WHERE id="{list_id}"'.format(list_id=list_id, site=site)
        self.dbpool.runOperation(statement)
        
    def get_start_urls(self, site):
        self.cursor.execute('SELECT * from detail_url WHERE site="%s"' % site)
        result = self.cursor.fetchall()
        urls = []
        for i in result:
            urls.append(i[1])
        return urls

class DetailDB(object):
    
    def __init__(self):
        self.dbpool = get_dbpool()

    def save(self, statement):
        self.dbpool.runOperation(statement)

