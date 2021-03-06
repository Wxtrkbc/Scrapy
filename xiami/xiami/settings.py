# -*- coding: utf-8 -*-

# Scrapy settings for xiami project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'xiami'

SPIDER_MODULES = ['xiami.spiders']
NEWSPIDER_MODULE = 'xiami.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'xiami (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'xiami.middlewares.XiamiSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'xiami.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'xiami.pipelines.XiamiPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'



HEADERS = {
    'Host': 'www.xiami.com',
    'Origin': 'www.xiami.com',
    'Referer': 'http://www.xiami.com/chart/index',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

}

DEFAULT_COOKIES = {
    "gid": "1488939715887",
    "join_from": "1zufSNtP6D010%2FjCCA",
    "_xiamitoken": "31bb5abb4d3ca338651a8057f2918247",
    "_unsign_token": "5dcc0eabceb4ed5128ab506cbb54067a",
    "cna": "LdroEAGrxjICAXzPsZLLmJzc",
    "bdshare_firstime": "1489043605046",
    "UM_distinctid": "15ac572ea20c50-0a80dd844a3dc-36627f00-384000-15ac572ea211cd",
    "CNZZDATA921634": "cnzz_eid%3D275186345-1488937592-null%26ntime%3D1489369605",
    "CNZZDATA2629111": "cnzz_eid%3D979814157-1488938324-null%26ntime%3D1489371041",
    "l": "AhcXOVgD6D1bk66qYR/7UDTrJ4FhEOu-",
    "isg": "AqioB1STZI2XBkhweA-ZrgKUeZC-9wzbn33YNGLZuCMWvUknCuXda60_w-K3"
}
