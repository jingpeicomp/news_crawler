# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import types

from leancloud import Object, Query
from scrapy import log


class NewsCrawlerPipeline(object):
    settings = None
    News = None

    def process_item(self, item, spider):
        if isinstance(item, (types.GeneratorType, types.ListType)):
            for each in item:
                self.process_item(each, spider)
        else:
            log.msg('NewsCrawlerPipeline begin to process item {0}'.format(item), 'INFO')
            self.__save(item)
            return item

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        ext.settings = crawler.settings
        ext.News = Object.extend(crawler.settings.get('LEANCLOUD_OBJECT_NAME'))

        return ext

    def __save(self, item):
        """
        保存抓取的数据
        :param item:
        :return:
        """
        query = Query(self.News)
        query.equal_to('newsId', item['newsId'])
        if query.count():
            log.msg('News has exist with same newsId {0}'.format(item['newsId']), 'INFO')
            return
        news = self.News()
        for key in item:
            news.set(key, item.get(key))
        news.save()
