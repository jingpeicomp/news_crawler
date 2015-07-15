# coding=utf-8
from re import search
import time
from datetime import datetime

from scrapy import Spider, Request

from news_crawler.items import NewsCrawlerItem


__author__ = 'liuzhaoming'


class HupuSpider(Spider):
    """
    虎扑体育爬虫
    """
    name = 'hupu'
    allowed_domains = ["m.hupu.com"]
    start_urls = [
        "http://m.hupu.com/soccer", "http://m.hupu.com/nba", "http://m.hupu.com/soccer", "http://m.hupu.com/cba/news",
        "http://m.hupu.com/soccer/news"
    ]
    root_domain = 'http://m.hupu.com'
    id_prex = 201

    def parse(self, response):
        # 获取文章
        return self.parse_category(response)

    def parse_category(self, response):
        # 获取文章
        article_url_list = response.xpath(
            '/html/body//a[contains(@href, "m.hupu.com/") '
            ' and contains(@href, "/news/") and contains(@href, ".html") ]/@href').extract()
        article_url_request_list = map(lambda article_url: Request(article_url, self.parse_article),
                                       article_url_list)

        # 获取栏目的页码
        # last_page_url = \
        # response.xpath('//div[@id="J_page"]//a[contains(@dace-node,"lastpage")]/@href').extract()[
        # 0]
        # last_page_num = int(last_page_url[last_page_url.rfind('/') + 1:])
        # page_url_prfx = last_page_url[:last_page_url.rfind('/') + 1]
        # page_request_list = map(lambda page_url: Request(page_url_prfx + page_url, self.parse_category),
        # xrange(last_page_num))
        return article_url_request_list

    def parse_article(self, response):
        # 处理文章页面
        item = NewsCrawlerItem()
        item['channel'] = 2
        item['source'] = u'虎扑'
        item['source_url'] = response.url
        # 从文章url中解析出虎扑文章ID
        huxiu_article_id = self.unbind_variable('/(?P<article_id>\\d+).html', 'article_id', item['source_url'])
        # 文章的ID用 虎嗅媒体的ID+虎嗅文章ID
        item['newsId'] = self.id_prex * 10000000 + int(huxiu_article_id)
        item['id'] = item['newsId']
        title_list = response.xpath('//header[@class="artical-title"]//h1[@class="headline"]/text()').extract()
        item['title'] = title_list[0] if title_list else response.xpath('/html/head/title/text()').extract()[0]
        time_str_list = response.xpath(
            '//header[@class="artical-title"]//span[@class="times"]/text()').extract()
        time_str = time_str_list[0].strip() if time_str_list else ''
        # 虎嗅时间格式为：48分钟前， 5小时前，  07-03 19:24
        item['publishTime'] = self.get_hupu_time(time_str)
        item['tags'] = response.xpath(
            '//section[@class="detail-content"]//div[contains(@class, "hot-tags")]//div[@class="swiper-slide"]/a/text()').extract()
        big_pic_list = response.xpath(
            '//section[@class="detail-content"]/article[@class="article-content"]/img/@src').extract()
        if big_pic_list:
            item['picOne'] = big_pic_list[0]
        if len(big_pic_list) > 1:
            item['picTwo'] = big_pic_list[1]
        if len(big_pic_list) > 2:
            item['picThr'] = big_pic_list[2]
        pic_list = big_pic_list
        item['picListString'] = ','.join(pic_list)
        item['picList'] = pic_list
        item['isLarge'] = True
        return item

    @staticmethod
    def unbind_variable(regex_expr, variable_name, text):
        """
        字符串中变量解绑定
        :param regex:
        :param variable_name:
        :param text:
        :return:
        """
        m = search(regex_expr, text)
        if not m:
            return None
        variable_value = m.group(variable_name)
        return variable_value

    def get_hupu_time(self, time_str):
        """
        解析虎扑时间格式，格式为48分钟前， 5小时前，  07-03 19:24
        :param time_str:
        :return:
        """
        time_stamp = int(time.time())
        minute = self.unbind_variable(u'(?P<number>\\d+)\u5206\u949f\u524d', 'number', time_str)
        if minute:
            return time_stamp - int(minute) * 60

        hours = self.unbind_variable(u'(?P<number>\\d+)\u5c0f\u65f6\u524d', 'number', time_str)
        if hours:
            return time_stamp - int(hours) * 60 * 60

        return int(time.mktime(datetime.strptime(time_str, '%m-%d %H:%M').timetuple()))




