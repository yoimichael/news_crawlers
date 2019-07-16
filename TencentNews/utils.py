#-*- coding: utf-8 -*-

import logging
import traceback
import time
import datetime
import requests
import os

logging.basicConfig(filename='crawl.log')

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
    directory =  ("./back_up/news_pictures/" +
            date + "/" +
            group + "/")
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    return directory
def download_imgs(urls, directory, news_id):
    '''
    下载保存标题缩略图和文章里的插图
    '''
    img_no = 0
    err_counter = 0 
    err = None
    
    for url in urls:
        # 把//开头的url改成http://
        if not "http" in url:
            url = url.replace("//","http://",1)
        img_no += 1
        img_loc = (directory + news_id + '-' + str(img_no) + ".jpg")
        is_saved, err = save_img(url, img_loc)
        err_counter += (not is_saved)
    
    # 如果有下载错误的
    if img_no != len(urls) or err_counter > 0:
        log(err,ERROR)
        self.fail_counter += 1

    return img_no