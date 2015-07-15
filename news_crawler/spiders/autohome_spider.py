# coding=utf-8
from re import search
import time
from datetime import datetime

from scrapy import Spider, Request

from news_crawler.items import NewsCrawlerItem


__author__ = 'liuzhaoming'


class AutohomeSpider(Spider):
    """
    汽车之家爬虫
    """
    name = 'autohome'
    allowed_domains = ["m.autohome.com.cn"]
    start_urls = [
        "http://m.autohome.com.cn/channel/"
    ]
    root_domain = 'http://m.autohome.com.cn'
    id_prex = 203

    def parse(self, response):
        # 获取文章
        return self.parse_category(response)

    def parse_category(self, response):
        # 获取文章
        article_url_list = response.xpath(
            '//ul[@id="list"]/li/a[contains(@href, ".html")]/@href').extract()
        article_url_request_list = map(lambda article_url: Request(self.root_domain + article_url, self.parse_article),
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
        item['channel'] = 4
        item['source'] = u'汽车之家'
        item['source_url'] = response.url
        # 从文章url中解析出虎扑文章ID
        huxiu_article_id = self.unbind_variable('/(?P<article_id>\\d+).html', 'article_id', item['source_url'])
        # 文章的ID用 虎嗅媒体的ID+虎嗅文章ID
        item['newsId'] = self.id_prex * 10000000 + int(huxiu_article_id)
        item['id'] = item['newsId']
        title_list = response.xpath('//div[@class="article-title"]/h1/text()').extract()
        item['title'] = title_list[0] if title_list else response.xpath('/html/head/title/text()').extract()[0]
        time_str_list = response.xpath('//div[@class="article-title"]/p/text()').extract()
        time_str = time_str_list[0].strip() if time_str_list else ''
        # 汽车之家时间格式为：类型:原创  2015-07-05  汽车之家  编辑:
        item['publishTime'] = self.get_time(time_str)
        big_pic_list = response.xpath(
            '//div[@class="article-content"]/p/img[contains(@data-src, ".autoimg.cn/")]/@data-src').extract()
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

    def get_time(self, time_str):
        """
        解析时间格式，格式为  "类型:原创  2015-07-05  汽车之家  编辑:"
        :param time_str:
        :return:
        """
        date_str = self.unbind_variable(r'(?P<number>\d+-\d+-\d+)', 'number', time_str)
        return int(time.mktime(datetime.strptime(date_str, '%Y-%m-%d').timetuple()))




