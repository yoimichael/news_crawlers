database_name = "news"
development_database_config = { 
    "user": "root", 
    "passwd": "dongjian",

    "host": 'localhost',
    'charset':'utf8',
    'use_unicode': True
}
table_name = "finance_news"
table_schema = (
    ("`id`", "CHAR(14)"), #目前一直是14
    ("`title`", "CHAR(40) NOT NULL"), #目前找到的最长是30
    ("`publish_time`", "DATETIME NOT NULL"), 
    ("`source`", "CHAR(20)"), #目前找到的最长是10
    ("`comment_num`", "MEDIUMINT UNSIGNED NOT NULL"), # 最大值有16777215
    ("`url`", "CHAR(60)"), #目前找到的最长是56，由于URL很有格式化，不会有长度大幅变化
    ("`keywords`", "TINYTEXT"), #目前找到的最长是24, TINYTEXT支持最大255
    ("`content`", "TEXT"), #目前找到的最长是373, TINYTEXT支持最大65535 
    ("`image_num`", "TINYINT UNSIGNED NOT NULL"), #最大值255
    ("`img_urls`", "TEXT"), #理由如下
    ("`img_locs`", "TEXT"), #理由如下
)
# image_num, img_locs数据库架构理由：
# 本地地址的格式是/back_up/news_pictures/0000-00-00/(20)/(14)-(3).jpg
# 一共77characters，假设最多有255个地址，这样78*255=最大有19890个characters
# 图片地址模版是https://inews.gtimg.com/newsapp_ls/0/9645825364_294195/0
# 一共55个characters， 同样理由
# 所以选择TEXT（最大值有65545）