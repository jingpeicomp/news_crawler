# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    newsCategoryId = scrapy.Field()
    newsCategory = scrapy.Field()
    mark = scrapy.Field()
    commentNum = scrapy.Field()
    id = scrapy.Field()
    newsId = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    source_url = scrapy.Field()
    publishTime = scrapy.Field()
    summary = scrapy.Field()
    newsAbstract = scrapy.Field()
    comment = scrapy.Field()
    local = scrapy.Field()
    picListString = scrapy.Field()
    picOne = scrapy.Field()
    picTwo = scrapy.Field()
    picThr = scrapy.Field()
    picList = scrapy.Field()
    isLarge = scrapy.Field()
    readStatus = scrapy.Field()
    collectStatus = scrapy.Field()
    likeStatus = scrapy.Field()
    interestedStatus = scrapy.Field()
    tags = scrapy.Field()
    type = scrapy.Field()
    channel = scrapy.Field()
    auto_tags = scrapy.Field()


