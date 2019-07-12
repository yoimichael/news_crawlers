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
    ("`comment_num`", "MEDIUMINT UNSIGNED NOT NULL"), # 最大值有8388607
    ("`url`", "CHAR(60)"), #目前找到的最长是56，由于URL很有格式化，不会有长度大幅变化
    ("`keywords`", "TINYTEXT"), #目前找到的最长是24, TINYTEXT支持最大255
    ("`content`", "TEXT"), #目前找到的最长是373, TINYTEXT支持最大65535 
)

# 所有和财经有关的新闻类别
keys = (
    {"chn":"财经","cid":"25","name":"finance"},
    {"chn":"公司","cid":"2501","name":"finance_company"},
    {"chn":"创业","cid":"2502","name":"finance_startup"},
    {"chn":"经济","cid":"2503","name":"finance_economy"},
    {"chn":"消费","cid":"2504","name":"finance_consume"},
    {"chn":"房地产","cid":"2505","name":"finance_estate"},
    {"chn":"投资","cid":"2506","name":"finance_investment"},
    {"chn":"理财","cid":"2507","name":"finance_mngmoney"},
    {"chn":"财经人物","cid":"2508","name":"finance_people"},
    {"chn":"产经","cid":"2509","name":"finance_business"},
    {"chn":"股市","cid":"2510","name":"finance_stock"},
    {"chn":"金融","cid":"2511","name":"finance_banking"},
    {"chn":"收藏","cid":"2512","name":"finance_collection"}
)