# -*- coding: utf-8 -*-

# this pipeline saves data into the database
from SqlHelper import SqlHelper
from scrapy.exceptions import DropItem
import config

class DataPipeline(object):

    def __init__(self, *args, **kwargs):
        # 数据管理方法
        self.sql = SqlHelper()
        self.create_table()
        # 缓存
        self.columns = [col.strip('`') for col, _ in config.table_schema]
        table_schema = config.table_name + "(" + ",".join(self.columns)+ ")" 
        # REPLACE 是让爬虫得到最新的评论数量，如果数据库里没有，INSERT
        self.insert_command = (
            "REPLACE INTO {} "
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ".format(table_schema)
        )

        # 异常数量
        self.fail_counter = 0

    def create_table(self):
        '''
        创建表格如果它不在数据库里
        '''
        schema = ",".join(" ".join(pair) for pair in config.table_schema)
        command = ( "CREATE TABLE IF NOT EXISTS " + 
                    config.table_name + "(" + schema + ",PRIMARY KEY(id)) ENGINE=INNODB;")
        self.sql.create_table(command)

    def process_item(self, item, spider):
        
        # 统计下载图片数量和记录异常数量 3 
        # self.fail_counter += 1 if err else 0 
        # self.img_downloaded += img_num

        # store to database
        data = {key: item[key] if key in item else "" for key in item.fields}
        data['image_num'] = len(data['img_urls'])
        data['img_urls'] = '@'.join(data['img_urls'])
        data['img_locs'] = '@'.join(data['img_locs'])
        self.store(data)

        return item

    def store(self, data):
        
        # 存进数据库
        insert_data = tuple(data[key] for key in self.columns)
        success = self.sql.insert_data(self.insert_command , insert_data)

        if not success:
            raise DropItem("SQL store error")
        
        

# startSpider(tencent:)
#         # 只更新没有存过的新闻
#         self.get_new = bool(getattr(self, 'get_new', False))
#         self.savedIDs = set() # 存已经存过的新闻id
    
#     def reset_stats(self):
#         # *******本地统计*******
#         # 数据库原本数量
#         self.rows_before = self.sql.get_num_rows()
#         # 下载图片数量
#         self.img_downloaded = 0

#     def update_saved_id(self):
#         '''
#         今天有哪些新闻被存过
#         '''
#         command = ('select id from ' + config.table_name + 
#                     ' where publish_time LIKE "' + 
#                     self.date.isoformat().split('T')[0] + '%"')
#         res = self.sql.query(command)
#         res = [] if not res else res
#         self.savedIDs = set([rows[0] for rows in res])

#     def log_summary(self):
#         # 总结本次爬取数据
#         try:
#             s = "\n********************\n"
#             summary = ""
#             headers = ['item_scraped_count(Links)','Abnormal','New data added','Image downloads']
#             data = [self.fail_counter, 
#                     self.num_new_rows(), 
#                     self.img_downloaded]
            
#             for header, data in zip(headers, data):
#                 summary += header + ": " + str(data) + "\n"
#             summary = s + summary + s
#             utils.log(summary, WARNING)
#         except Exception:
#             utils.log("\nSpider exited abnormally", WARNING)

#     def num_new_rows(self):
#         # 爬完之后更新加了多少条数据
#         rows_now = self.sql.get_num_rows()
#         if self.rows_before and rows_now:
#             added = rows_now - self.rows_before
#         else:
#             added = "Get_num_row error"
#         self.rows_before = rows_now
#         return added


