# Tencent News Crawler using Spiderkeeper, Scrapyd, Supervisor

## Usage
- For past news data, pass in the argument ```days_prior``` to specify how many days before do you want the spider to start crawling. (Drawback: the API weblink available only supports news about 20 days before the current date.)
- For current data, don't pass in anything.

## Spiders:
### FinanceSpider 
This crawler uses API enpoints implemented within Tencent New's auto-scroll feature in order to crawl and store all key information about news related to finance. 

## MySQL database schema
Database name: news
Table name: finance_news
+--------------+-----------------------+------+-----+---------+-------+
| Field        | Type                  | Null | Key | Default | Extra |
+--------------+-----------------------+------+-----+---------+-------+
| id           | char(14)              | NO   | PRI | NULL    |       |
| title        | char(40)              | NO   |     | NULL    |       |
| publish_time | datetime              | NO   |     | NULL    |       |
| source       | char(20)              | YES  |     | NULL    |       |
| comment_num  | mediumint(8) unsigned | NO   |     | NULL    |       |
| url          | char(60)              | YES  |     | NULL    |       |
| keywords     | tinytext              | YES  |     | NULL    |       |
| content      | text                  | YES  |     | NULL    |       |
+--------------+-----------------------+------+-----+---------+-------+

## Findings on Tencent News's URLs
1. https://pacaio.match.qq.com/xw/site?&ext=finance&num=20&page=0
    - Returns a list of information-rich json file of news that has "finance" in its "ext" field
    - for exaple, one news can have its "ext" field be:
    ```
        "349+0"+"all":";;;734+9"+"3h":"106587+4680;1447+23;stock:8168+349#finance:51062+2578;674+9"+"day":"361497+15793;8179+104;stock:29103+1240#finance:176307+8396;734+9"
    ```
    - which looks like a result of machine-learned catagory analysis

2. http://pacaio.match.qq.com/openapi/json?key=finance:20190709&num=20&page=0
    - (Accepted)
    - Also used by auto-scroll on the website
    - Returns a concise list of news according to the given date and category
    - Categories of finance:
    ```
    ['finance', # used by 财经网
    'finance_company',
    'finance_startup',
    'finance_economy',
    'finance_consume',
    'finance_estate',
    'finance_investment',
    'finance_mngmoney',
    'finance_people',
    'finance_business',
    'finance_stock',
    'finance_banking',
    'finance_collection']
    ```


## Python dependences (pip install)

|         Package        |                 Why                |
+------------------------+------------------------------------+
|         scrapy         |            for crwalers            |
|         logging        |              for logs              |
|        traceback       |      for debug tracing in logs     |
| mysql-connector-python | for SHA2 password auth to mysql db |
| scrapyd & spiderkeeper | for crawler monitoring and control | 
supervisor

## Known bug

1. Spiderkeeper doesn't show up the list of spiders available:
    run scrapyd-deploy in directory to manually deploy
