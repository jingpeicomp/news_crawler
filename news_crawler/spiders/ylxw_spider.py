# coding=utf-8
from re import search
import time
from datetime import datetime

from scrapy import Spider, Request

from news_crawler.items import NewsCrawlerItem


__author__ = 'liuzhaoming'


class YlxwSpider(Spider):
    """
    娱乐新闻爬虫
    """
    name = 'ylxw'
    allowed_domains = ["m.news.yule.com.cn"]
    start_urls = [
        "http://m.news.yule.com.cn"
    ]
    root_domain = 'http://m.news.yule.com.cn'
    id_prex = 202

    def parse(self, response):
        # 获取文章
        return self.parse_category(response)

    def parse_category(self, response):
        # 获取文章
        article_url_list = response.xpath('/html/body//a[contains(@href, "/c/")]/@href').extract()
        article_url_list = filter(
            lambda article_url: search(r'/c/[\d]+/[\d]+.html', article_url), article_url_list)
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
        item['channel'] = 3
        item['source'] = u'中国娱乐网'
        item['source_url'] = response.url
        # 从文章url中解析出虎扑文章ID
        huxiu_article_id = self.unbind_variable('/(?P<article_id>\\d+).html', 'article_id', item['source_url'])
        # 文章的ID用 虎嗅媒体的ID+虎嗅文章ID
        item['newsId'] = self.id_prex * 10000000 + int(huxiu_article_id)
        item['id'] = item['newsId']
        title_list = response.xpath('/html/body/article/div[@class="articlecontent"]/h1/text()').extract()
        item['title'] = title_list[0] if title_list else response.xpath('/html/head/title/text()').extract()[0]
        time_str_list = response.xpath(
            '/html/body/article/div[@class="articlecontent"]/div[@class="tm"]/text()').extract()
        time_str = time_str_list[0].strip() if time_str_list else ''
        # 时间格式为：日期：2015-06-23 来源：
        item['publishTime'] = self.get_time(time_str)
        big_pic_list = response.xpath(
            '/html/body/article/div[@class="articlecontent"]/div[@class="content"]//'
            'img[contains(@src, "http://news.yule.com.cn/")]/@src').extract()
        if big_pic_list:
            item['picOne'] = big_pic_list[0]
        if len(big_pic_list) > 1:
            item['picTwo'] = big_pic_list[1]
        if len(big_pic_list) > 2:
            item['picThr'] = big_pic_list[2]
        pic_list = big_pic_list
        item['picListString'] = ','.join(pic_list)
        item['picList'] = pic_list
        item['isLarge'] = False
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
        解析时间格式，格式为  "日期：2015-06-23 来源："
        :param time_str:
        :return:
        """
        date_str = self.unbind_variable(r'(?P<number>\d+-\d+-\d+) ', 'number', time_str)
        return int(time.mktime(datetime.strptime(date_str, '%Y-%m-%d').timetuple()))




