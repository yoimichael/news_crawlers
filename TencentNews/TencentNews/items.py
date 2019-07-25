# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst, Identity

def add_http(url):
    if "http" not in url:
        return url.replace("//","http://",1)
    return url

def normalize_content(selector):
    '''
    get a selector on one paragraph
    return raw texts of this news with images replaced by a '#'
    '''
    paragraph = ''.join(selector.css('::text').extract())
    paragraph = paragraph.strip()
    paragraph += len(selector.css('img')) * "#" # '#' 表示图片    
    return paragraph

# here defines the input/output processer for TencentNewsItem
class TencentNewsItemLoader(ItemLoader):
    # since all inputs passed to item fields are lists
    # take the first one and the only one
    default_output_processor = TakeFirst()
    # defines a extractor and a separator for keywords
    keywords_in = MapCompose(lambda x: x[0])
    keywords_out = Join('|')
    # normalize content according to rules specified above
    content_in = MapCompose(normalize_content)
    content_out = Join('\n')
    # add http if it doesn't exist
    img_urls_in = MapCompose(add_http)
    img_urls_out = Identity()

class TencentNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # can be accessed like a dictoinary item['news_id']
    id = scrapy.Field()
    title = scrapy.Field()
    publish_time = scrapy.Field()
    source = scrapy.Field()
    comment_num = scrapy.Field()
    url = scrapy.Field()
    keywords = scrapy.Field()
    content = scrapy.Field()
    # urls to download for ImagePipeline 
    img_urls = scrapy.Field()
    img_locs = scrapy.Field() 
    img_group = scrapy.Field()

    def __repr__(self):
        """only print out id after exiting the Pipeline"""
        return repr({"id": str(self['id'])})
    

