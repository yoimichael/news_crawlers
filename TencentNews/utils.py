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

    