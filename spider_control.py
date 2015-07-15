# encoding=utf-8
import time

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

####爬虫的名称
MY_SPIDER_NAMES = ['hupu', 'autohome', 'huxiu', 'ylxw']
####爬虫对应的模块
MY_SPIDER_MODULES = {  # 'AmazonBookSpider': 'scrapy_barcode.spiders.amzon_book_spider.AmazonBookSpider',
                       'hupu': 'news_crawler.spiders.hupu_spider.HupuSpider',
                       'autohome': 'news_crawler.spiders.autohome_spider.AutohomeSpider',
                       'huxiu': 'news_crawler.spiders.huxiu_spider.HuxiuSpider',
                       'ylxw': 'news_crawler.spiders.ylxw_spider.YlxwSpider'}

scheduler = BackgroundScheduler()


class Receiver:
    countdown = 0

    def __init__(self, countdown):
        self.countdown = countdown

    def stop(self):
        self.countdown -= 1
        if self.countdown <= 0:
            reactor.stop()


def set_crawler(spider, receiver):
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(receiver.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()


def get_class(module_name):
    parts = module_name.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def spider_start():
    print 'spider_start called'
    receiver = Receiver(len(MY_SPIDER_NAMES))
    for spider_name in MY_SPIDER_NAMES:
        cls = get_class(MY_SPIDER_MODULES.get(spider_name))
        spider = cls()
        set_crawler(spider, receiver)
    reactor.run()


def apscheduler_listener(event):
    """
    apscheduler监听器
    :param event:
    :return:
    """
    if event.exception:
        print('The job crashed : {0}', event.job_id)
    else:
        print('The job worked : {0}', event.job_id)


def spider_period_start(minutes=15, start_hour=9, end_hour=20):
    trigger = CronTrigger(hour='{0}-{1}'.format(start_hour, end_hour), minute='*/{0}'.format(minutes))
    scheduler.add_job(spider_start, trigger)
    scheduler.add_listener(apscheduler_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()


if __name__ == '__main__':
    spider_start()
    spider_period_start()
    while 1:
        time.sleep(10)