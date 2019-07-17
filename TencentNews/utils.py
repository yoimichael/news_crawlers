#-*- coding: utf-8 -*-

import logging
import traceback
import time
import datetime
import requests
import os

logging.basicConfig(filename='crawl.log')

image_dir = "./back_up/news_pictures/"

def log(message, level=logging.DEBUG, *args, **kwargs):
    
    logging.log(level, message, *args, **kwargs)

    if level == logging.WARNING or level == logging.ERROR:
        print('%s::[%s]\t%s' % 
            (
            datetime.datetime.now().isoformat()[:10],
            level,
            message
            )
        )
        if level == logging.ERROR:
            msg = "".join(traceback.format_stack())
            logging.log(level, msg, *args, **kwargs)

def save_img(url, local_addr):
    try:
        img_data = requests.get(url).content
        with open(local_addr, 'wb') as handler:
            handler.write(img_data)
        return True, None
    except Exception as e:
        return False, e
        
def img_dir(date, group):
    directory =  image_dir + date + "/" + group + "/"
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    return directory
def download_imgs(urls, directory, news_id):
    '''
    下载保存标题缩略图和文章里的插图
    return:
        1. (string) image urls joined by '@'
        2. (string) image locations on disk joined by '@'
        3. (int) num of image downloaded
        4. err object if error happened during save_img()
    '''
    img_no = 1
    err = None
    img_urls = []
    img_locs = []

    for url in urls:
        img_loc = (directory + news_id + '-' + str(img_no) + ".jpg")
        is_saved, err = save_img(url, img_loc)
        if is_saved:
            img_urls.append(url)
            img_locs.append(img_loc)
            img_no += 1

        # TODO: unused error counter
        # err_counter += (not is_saved)
    
    # 如果有下载错误的
    if img_no-1 != len(urls):
        log(err,logging.ERROR)
    
    return ('@'.join(img_urls),
            '@'.join(img_locs),
            img_no-1,
            err)