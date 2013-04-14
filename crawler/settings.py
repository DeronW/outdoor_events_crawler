BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

USER_AGENT = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3)"

ITEM_PIPELINES = [
    'crawler.pipelines.ListSavePipeline',
    'crawler.pipelines.DetailFilterPipeline',
    'crawler.pipelines.DetailSavePipeline',
]

SPIDER_MIDDLEWARES = {
    #'crawler.middlewares.RepeatUrlMiddleware': 543,
}

EXTENSIONS = {
    'crawler.extensions.ErrorSignal': 0,
}
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [400, 401, 404, 500, 502, 503, 504]

# DB SET
DB_HOST = '192.168.12.230'
DB_USERNAME = 'search'
DB_PASSWORD = 'lvye'
DB_DBNAME = 'search_mid'
DB_PORT = 3306
DB_CHARSET = 'utf8'

MAIN_SPIDER = (
    'c', 
    'y'
)
ACTIVITY_SPIDER = (
    '',
)
