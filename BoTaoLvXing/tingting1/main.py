# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import time
import os

while True:
    os.system("scrapy crawl gg")
    time.sleep(120)  #每隔一天运行一次 24*60*60=86400s
