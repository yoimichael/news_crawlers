#-*- coding: utf-8 -*-

from json import loads
import scrapy
import datetime
from pytz import timezone
import utils
import TencentNews.helpers as hlpr
from logging import WARNING, ERROR
from TencentNews.items import TencentNewsItem, TencentNewsItemLoader

class FinanceSpider(scrapy.Spider):
    name = "FinanceSpider" 
    
    def __init__(self, *args, **kwargs):
        '''
        days_prior: 从今天的几天前开始？
        '''
        super(FinanceSpider, self).__init__(*args, **kwargs)

        # 设置开始日期(基于中国时区)
        self.tz = timezone(zone='Asia/Chongqing')
        date = datetime.datetime.now(tz=self.tz)
        days_prior=int(getattr(self, 'days_prior', 0))
        print("从%d天前开始爬" % days_prior)
        self.date = date - datetime.timedelta(days=days_prior)
    
        # 提前结束
        self.get_new = bool(getattr(self, 'early_stop', False))
        
        # 异常数量
        self.fail_counter = 0

    def uptoDate(self):
        '''
        是否已经爬完今天
        '''
        return (datetime.datetime.now(tz=self.tz)-self.date).days < 0

    def start_requests(self):
        # 爬到今天
        while not self.uptoDate():  

            # 爬取当天所有和finance有关的分类
            for category in hlpr.keys:
                key = category['name']
                
                # TODO: 爬取所有pages （不确定可不可以一个page完成）
                self.all_pages_done = False
                for i in range(9999):
                    if self.all_pages_done:
                        break
                    
                    url = hlpr.make_url(self.date, i, key)
                    # TODO:: errback不一定是要加一
                    yield scrapy.Request(   url, 
                                            callback=self.parse,
                                            errback=self.error_parse
                                        )

            # 进入下一天
            self.date += datetime.timedelta(days=1)

    def parse(self, response):
        '''
        爬取网址里的json 
        '''
        all_news = loads(response.body)['data']
        if not all_news:
            # 如果本天的新闻看完了，再进入下一天
            self.all_pages_done = True
            return

        # 读取重要消息
        for news_data in all_news:
            
            # TODO:: check early-stop

            # 爬取新闻内容    
            request = scrapy.Request(   news_data['url'], 
                                        callback=self.parse_news_content,
                                        errback=self.error_parse
                                    )
            # 同时把news object传过去
            request.meta['news_data'] = news_data
            yield request

    def parse_news_content(self,response):
        '''
        itemize all data about this news
        '''
        # news data
        news = response.meta['news_data'] 
        
        img_urls = [url for urls in news['irs_imgs'].values() for url in urls]
        img_urls.extend(response.css(".one-p img::attr(src)").extract())
        
        il = TencentNewsItemLoader(item=TencentNewsItem())
        il.add_value('id', news['id'])
        il.add_value('title', news['title'])
        il.add_value('publish_time', news['publish_time'])
        il.add_value('source', news['source'])
        il.add_value('comment_num', news['comment_num'])
        il.add_value('url', news['url'])
        il.add_value('keywords', news['tag_label'])
        il.add_value('img_urls', img_urls)
        il.add_value('content', response.css('.one-p'))
        il.add_value('img_group', 'tencent_news')

        return il.load_item()

    def error_parse(self, failure):
        utils.log(failure.request.meta,ERROR)
        self.fail_counter += 1
