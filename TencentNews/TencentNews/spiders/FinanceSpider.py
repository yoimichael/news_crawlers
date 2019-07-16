#-*- coding: utf-8 -*-

from json import loads
import scrapy
import datetime
from pytz import timezone
import utils
import config
from SqlHelper import SqlHelper
from logging import WARNING, ERROR

class FinanceSpider(scrapy.Spider):
    name = "FinanceSpider"
    BASE_URL = "http://pacaio.match.qq.com/openapi/json?"
    MAX_page = 9999
    date = None 
    
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
        
        # 数据库
        self.initialize_db()

    def get_num_rows(self):
        # 得取数据库有多少行数据点
        command = "SELECT COUNT(*) FROM " + config.table_name
        res = self.sql.query_one(command)
        if res:
            return res[0]
        return None

    
    def initialize_db(self):
        # 数据管理方法
        self.sql = SqlHelper()
        self.create_table()
        # 异常数量
        self.fail_counter = 0
        # 缓存
        self.columns = [col.strip('`') for col, _ in config.table_schema]
        table_schema = config.table_name + "(" + ",".join(self.columns)+ ")" 
        # REPLACE 是让爬虫得到最新的评论数量
        self.insert_command = (
            "REPLACE INTO {} "
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) ".format(table_schema)
        )

    def create_table(self):
        schema = ",".join(" ".join(pair) for pair in config.table_schema)
        command = ( "CREATE TABLE IF NOT EXISTS " + 
                    config.table_name + "(" + schema + ",PRIMARY KEY(id)) ENGINE=INNODB;")
        self.sql.create_table(command)

    def make_url(self,page,key,num=50):
        '''
        组成完整的URL
        '''
        url = self.BASE_URL
        url += "key=" + key + ":" + self.format_date()
        url += "&num=" + str(num) 
        url += "&page=" + str(page) 
        return url

    def format_date(self):
        '''
        用腾讯用的日期格式
        '''
        return self.date.isoformat().split('T')[0].replace('-','')
        # return "%.4d%.2d%.2d" % (y,m,d)

    def uptoDate(self):
        '''
        是否已经爬完到今天
        '''
        return (datetime.datetime.now(tz=self.tz)-self.date).days < 0
    
    def reset_stats(self):
        # *******本地统计*******
        # 默认每页数量
        self.num = 50
        # 爬取新闻总数
        self.total = 0
        # 数据库原本数量
        self.rows_before = self.get_num_rows()
        # 下载图片数量
        self.img_downloaded = 0

    def start_requests(self):
        self.reset_stats()

        # 爬到今天
        while not self.uptoDate():  
            # 爬取当天所有和finance有关的分类
            for category in config.keys:
                key = category['name']
                
                # TODO: 爬取所有pages （不确定可不可以一个page完成）
                self.all_pages_done = False
                for i in range(self.MAX_page):
                    if self.all_pages_done:
                        break
                    
                    url = self.make_url(i,key)
                    # TODO:: errback不一定是要加一
                    yield scrapy.Request(url, 
                                        callback=self.parse_news_json,
                                        errback=self.error_parse
                                        )
            
            # 进入下一天
            self.date += datetime.timedelta(days=1)
            print("进入下一天，目前爬取数量：%d" % self.total)

        # 爬完之后更新加了多少条数据
        rows_now = self.get_num_rows() 
        if self.rows_before and rows_now:
            self.added = rows_now - self.rows_before
        else:
            self.added = "Get_num_row error"

    def parse_news_json(self, response):
        # 读取重要消息
        for news_data in self.parse(response):
            # 爬取新闻内容    
            news_url = news_data['url']
            request = scrapy.Request(news_url, 
                                    callback=self.parse_news_http,
                                    errback=self.error_parse
                                    )
            # 同时把news_data传过去
            request.meta['news_data'] = news_data
            yield request

    def parse_news_http(self,response):
        
        # news data
        news_data = response.meta['news_data'] 
        
        # 图片地址
        urls = (news_data['image_url'] + 
                response.css(".one-p img::attr(src)").extract())
        date = news_data['publish_time'][:10]
        directory = utils.img_dir(date, 'tencent_news')
        news_id = news_data['id']
        # 下载图片
        img_no = utils.download_imgs(urls,directory,news_id)
        # 统计下载图片数量
        self.img_downloaded += img_no
        
        # 爬取新闻内容    
        content = ""
        for s in response.css('.one-p::text').extract():
            s = s.strip()
            content += s + '\n' if s else ""

        # 存进数据库
        news_data['content'] = content
        news_data['image_num'] = img_no
        self.store(news_data)

    def error_parse(self, failure):
        # 记录异常数量 1
        utils.log(failure.request.meta,ERROR)
        self.fail_counter += 1

    def store(self, data):
        self.total += 1
        
        # 存进数据库
        insert_data = tuple(data[key] for key in self.columns)
        # TODO:
        # command = (self.insert_command +
        #             "ON DUPLICATE KEY UPDATE " + 
        #             'comment_num=' + str(data['comment_num']))   

        success = self.sql.insert_data(self.insert_command , insert_data)

        # 记录异常数量 2
        self.fail_counter += (not success)

    def parse(self, response):
        data = loads(response.body)['data']
        if not data:
            # 如果本天的新闻看完了，再进入下一天
            self.all_pages_done = True
            return
            
        for news in data:
            yield {
                'id': news['id'],
                'title': news['title'],
                'publish_time': news['publish_time'],
                'source': news['source'],
                'comment_num': news['comment_num'],
                'url': news['url'],
                'keywords': "|".join(t[0] for t in news['tag_label']),                
                'image_url': [url for urls in news['irs_imgs'].values() for url in urls]
            }    


    def __del__(self):
        # 总结本次爬取数据
        try:
            s = "\n********************\n"
            summary = ""
            headers = ['Links','Abnormal','New data','Image downloads']
            data = [self.total, self.fail_counter, self.added, self.img_downloaded]
            for header, data in zip(headers, data):
                summary += header + ": " + str(data) + "\n"
            summary = s + summary + s
            utils.log(summary, WARNING)
        except Exception:
            utils.log("\nSpider exited abnormally", WARNING)