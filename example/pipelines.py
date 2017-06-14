# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import json
from scrapy import signals
# from pybloomfilter import BloomFilter
from . import settings
from scrapy.exceptions import DropItem

class ExamplePipeline(object):
    """This pipeline class object is designed for ElasticSearch client
    """

    def process_item(self, item, spider):
        return item

    def __del__(self):
        # self.storage.close()
        self.searchIndex.finish_index()
