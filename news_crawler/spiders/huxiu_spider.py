# coding=utf-8
from re import search
from datetime import datetime
import time

from scrapy import Spider, Request

from news_crawler.items import NewsCrawlerItem


__author__ = 'liuzhaoming'


class HuxiuSpider(Spider):
    """
    虎嗅新闻爬虫
    """
    name = 'huxiu'
    allowed_domains = ["huxiu.com"]
    start_urls = [
        "http://wwww.huxiu.com/focus"
    ]
    root_domain = 'http://wwww.huxiu.com'
    id_prex = 1011

    def parse(self, response):
        # 获取文章
        return self.parse_category(response)

    def parse_category(self, response):
        # 获取文章
        article_url_list = response.xpath('/html/body//a[contains(@href, "/article/")]/@href').extract()
        article_url_request_list = map(lambda article_url: Request(self.root_domain + article_url, self.parse_article),
                                       article_url_list)

        # 获取栏目的页码
        # page_url_list = response.xpath('/html/body//div[@id="page_list"]//ul[@class="pagination"]/li/a/@href').extract()
        # page_request_list = map(lambda page_url: Request(self.root_domain + page_url, self.parse_category),
        # page_url_list)
        # 现在改为每次只抓前两页
        if not response.url.endswith('.html'):
            article_url_request_list.append(Request('http://wwww.huxiu.com/focus/2.html', self.parse_category))
        return article_url_request_list

    def parse_article(self, response):
        # 处理文章页面
        item = NewsCrawlerItem()
        item['channel'] = 1
        item['source'] = u'虎嗅'
        item['source_url'] = response.url if response.url.endswith('/1.html') else '/1.html'.join((response.url, ''))
        # 从文章url中解析出虎嗅文章ID
        huxiu_article_id = self.unbind_variable('/article/(?P<article_id>\\d+)', 'article_id', item['source_url'])
        # 文章的ID用 虎嗅媒体的ID+虎嗅文章ID
        item['newsId'] = self.id_prex * 1000000 + int(huxiu_article_id)
        item['id'] = item['newsId']
        title_list = response.xpath('/html/body//div[@id="page_article"]//h1/text()').extract()
        item['title'] = title_list[0] if title_list else response.xpath('/html/head/title/text()').extract()[0]
        time_str_list = response.xpath(
            '/html/body//div[@id="page_article"]//time[@class="pull-left time"]/text()').extract()
        time_str = time_str_list[0].strip() if time_str_list else ''
        # 虎嗅时间格式为：2015-06-18 07:55
        item['publishTime'] = int(time.mktime(datetime.strptime(time_str, '%Y-%m-%d %H:%M').timetuple())
                                  if time_str else time.mktime(datetime.now().timetuple()))
        item['tags'] = response.xpath(
            '/html/body//div[@id="page_article"]//ul[@class="pull-left list-inline tag-box"]/li/a/text()').extract()
        big_pic_list = response.xpath('/html/body//div[@id="page_article"]//div[@class="big-pic"]/img/@src').extract()
        if big_pic_list:
            item['picOne'] = big_pic_list[0]
        if len(big_pic_list) > 1:
            item['picTwo'] = big_pic_list[1]
        if len(big_pic_list) > 2:
            item['picThr'] = big_pic_list[2]
        pic_list = response.xpath(
            '/html/body//div[@id="page_article"]//img[contains(@src,"huxiu.com/article/content/")]/@src').extract()
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
        return variable_value if variable_value else None



