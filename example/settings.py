# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = 'example.spiders'

USER_AGENT = 'scrapy-redis (+https://github.com/rolando/scrapy-redis)'

DOWLOAD_DELAY = 1

COOKIS_ENABLED = False
ITEM_PIPELINES = {
	'example.pipelines.ExamplePipeline' : 300,
	'scrapy_redis.pipelines.RedisPipeline' : 400
}
SCHEDULER_PERSIST = True
RETRY_TIMES = 1
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DOWNLOAD_TIMEOUT = 10
REDIS_HOST = 'cocopcopy.com'
REDIS_PORT = 6379
