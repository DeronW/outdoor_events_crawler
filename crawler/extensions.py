from scrapy import signals
from scrapy import log

class ErrorSignal(object):
    @classmethod
    def from_crawler(self, crawler):
      ext = self()
      crawler.signals.connect(ext.spider_error, signal=signals.spider_error)
      return ext

    def spider_error(self, failure, response, spider):
      log.err("Error on {0}, traceback: {1}".format(response.url, failure.getTraceback()))

