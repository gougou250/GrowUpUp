####波涛旅行抢券,将cookie统一写入一个文件中，从文件中读取各个账户的cookie值，每个账号一个进程，同时开始多个线程的账户请求
####波涛旅行抢券,将cookie统一写入一个文件中，从文件中读取各个账户的cookie值，每个账号一个进程，同时开始多个线程的账户请求
####波涛旅行抢券,将cookie统一写入一个文件中，从文件中读取各个账户的cookie值，每个账号一个进程，同时开始多个线程的账户请求

##    start_urls = ('http://mygifts.plateno.com/frontInterface/Shop_GetGoodsByCategory.do?categoryID=78&where=%7B%22startPoint%22%3A%22%22%2C%22endPoint%22%3A%22%22%2C%22keyword%22%3A%22%22%7D&sort=0&pageSize=20&pageIndex=1',)


import scrapy
from scrapy import Request
#from scrapy_splash import SplashRequest
#from scrapy import FormRequest
import json
import re
from tingting1.items import Tingting1Item
#from scrapy.selector import Selector
from bs4 import BeautifulSoup
import requests
import time
import random
import os                                            
#import time 
#import datetime
while True:
			itemID = '804'
			goodsDetailpage = 'http://mygifts.plateno.com/frontInterface/Shop_GetGoodsByID.do?itemID=%s&categoryID=78'%itemID##商品详情页的json链接
			r_detail = requests.get(goodsDetailpage)
			title = r_detail.json()['result']['itemName']
			vipstock = r_detail.json()['result']['itemVIPStock']
			if int(vipstock) != 0:
				os.system('scrapy crawl gg')
				print('执行结束')
				break
			print (vipstock)

            
            