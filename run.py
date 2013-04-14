from scrapy.cmdline import execute

from crawler import settings

for i in settings.MAIN_SPIDER:
    execute(['run.py', 'crawl', i])

for i in settings.ACTIVITY_SPIDER:
    execute(['run.py', 'crawl', i])

