import scrapy
import pymysql
import queue
import re
from urllib.parse import urlparse
from scrapy import signals
from scrapy.selector import HtmlXPathSelector
from example.items import ExampleItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider

class MyCrawler(RedisCrawlSpider):
	"""Spider that reads urls from redis queue (myspider:start_urls)."""
	name = 'mycrawler_redis'
	redis_key = 'mycrawler:start_urls'

	rules = (
			Rule(LinkExtractor(restrict_xpaths=('//div[@class="rightcontblock"]')), callback='parse_page', follow=True),
	)

	def __init__(self, *args, **kwargs):
		# Dynamically define the allowed domains list.
		# domain = kwargs.pop('domain', '')
		# self.allowed_domains = filter
		super(MyCrawler, self).__init__(*args, **kwargs)

	def parse_page(self, response):
		item = ExampleItem()
		item['url'] = response.url
		item['title'] = response.xpath('/html/head/title/text()').extract_first()
		m=re.match(r'(\d+)年(\d+)月份(\S+)\S车\(分制造商\)销量',item['title'])
		if m is not None:
		
			year=m.group(1)
			month=m.group(2)
			country=m.group(3)
			conn = pymysql.Connect(host='127.0.0.1',port=3306,user='root',passwd='123456',db='car',charset='utf8')
			trs2=response.xpath('//div[@class="newstext"]/table/tbody/tr/td[2]/font')
			trs=response.xpath('//div[@class="newstext"]/table/tbody/tr/td[1]/font')
			for tr in trs:
				i=trs.index(tr)
				logo=tr.xpath('string(.)').extract()[0]
				num=trs2[i].xpath('string(.)').extract()[0]
				sql= "insert into sale values('%s','%s','%s','%s','%s')" % (year,month,country,logo,num)
				cursor=conn.cursor()
				try:
					cursor.execute(sql)
				except:
					yield {'insert error': item['url']}
				cursor.close()
				yield {'logo':logo, 'num':num}
			yield {'year':year, 'month':month, 'country':country}
			conn.commit()
			conn .close()
		yield {'url': item['url'], 'name': item['title']}
		return item

