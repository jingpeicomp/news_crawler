# -*- coding: utf-8 -*-

# Scrapy settings for news_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
# http://doc.scrapy.org/en/latest/topics/settings.html
#
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

BOT_NAME = 'news_crawler'

SPIDER_MODULES = ['news_crawler.spiders']
NEWSPIDER_MODULE = 'news_crawler.spiders'

LOG_LEVEL = 'INFO'
LOG_FILE = 'news_scrapy.log'

ITEM_PIPELINES = {
    'news_crawler.pipelines.NewsCrawlerPipeline': 300
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
COOKIES_ENABLED = True

LEANCLOUD_APP_ID = '4lrycm58b7jgw0rfoxa03rdr7589eojojweu2ub0lihhxtzq'

LEANCLOUD_APP_KEY = 'cuyjnokfsi6vz4s87xu8u5b7p911fiur7tdm9a0p9d83w3i9'

LEANCLOUD_OBJECT_NAME = 'News'

# from gevent import monkey
#
# monkey.patch_all()

import leancloud

leancloud.init(LEANCLOUD_APP_ID, LEANCLOUD_APP_KEY)
