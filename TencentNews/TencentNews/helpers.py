# ******** helper functions and constants for Tencent news ********

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
def make_url(date,page,key,num=100): # 默认每页数量100
    '''
    组成完整的URL
    '''
    url = "http://pacaio.match.qq.com/openapi/json?"
    url += "key=" + key + ":" + formatted_date(date)
    url += "&num=" + str(num) 
    url += "&page=" + str(page) 
    return url

def formatted_date(date):
    '''
    用腾讯用的日期格式
    '''
    return date.isoformat().split('T')[0].replace('-','')
    # return "%.4d%.2d%.2d" % (y,m,d)
    