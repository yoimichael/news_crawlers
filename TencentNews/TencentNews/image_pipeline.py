# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
from utils import log
from logging import WARNING

class ImagePipeline(ImagesPipeline):
    # image pipeline converts images to jpg format and avoids re-downloading

    def close_spider(self, spider):
        log('move_err: %d' % self.move_err, WARNING)

    def __init__(self, *args, **kwargs):
        super(ImagePipeline, self).__init__(*args, **kwargs)
        
        self.move_err = 0

    def get_media_requests(self, item, info):
        
        for image_url in item['img_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        # Faster Alternative: give up the custom directory
        # file_paths = [x['path'] for ok, x in results if ok]

        storage = get_project_settings().get('IMAGES_STORE')
        custom_dir = os.path.join(storage, item['publish_time'][:10],item['img_group'])
        # create directory if doesn't exist (tested on mac not necessary)
        if not os.path.exists(custom_dir): 
            os.makedirs(custom_dir)
        
        img_locs = []
        num = 1
        # save local address of images 
        for ok, info in results:
            if not ok:
                raise DropItem("image not successfully downloaded/stored")

            path = os.path.join(storage, info['path'])
            target_path = os.path.join( custom_dir, 
                                        item['id'] + '-' + str(num) + '.jpg')
            # move image to custom directory
            try:
                os.rename(path, target_path)
            except OSError as e:
                # often caused by file at path already moved
                self.move_err += 1
                # raise DropItem("Move error: %r" % e)
            
            num += 1
            img_locs.append(target_path)
        
        item['img_locs'] = img_locs

        return item