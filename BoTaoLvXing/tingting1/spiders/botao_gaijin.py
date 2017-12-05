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
#import time 
#import datetime

class gougou(scrapy.Spider):
    name = 'gg'
    #allow_domains = ['weibo.com']
    #u_group = []
    #for p in range(1001,3240):
    #    u_jangxin = 'http://www.creditjx.gov.cn/datareporting/doublePublicity/queryDoublePublicityList.json?inpParam=&orgIdOrRegionId=&page=%s&pageSize=1000&tableType=1'%p
    #    u_group.append(u_jangxin)

    '''
    cookies1 = {
    'HttpOnly':'true',
    'CNZZDATA1256274125':'1640015372-1487174624-%7C1510799799',
    #'cookie_cart182122378':'32389fd588dd1628', ##不同账户cookie_cart的num不同，但是value相同？？？是否只是时间长了会过期？
    'JSESSIONID':'ABDD9B6F040288FBC1D23F15B59CF49F',
    'UM_distinctid':'15c25faaa4daa1-0f7b1d4287145d-36775c00-4a640-15c25faaa4ea73', ##和设备有关，一直未变
    }
    '''
    f = open('cookie2.txt','r') ##改动cookies变量的时候记得注意一下标点的中英文情况
    

    #start_urls = ('http://mygifts.plateno.com/frontInterface/Shop_GetGoodsByCategory.do?categoryID=78&where=%7B%22startPoint%22%3A%22%22%2C%22endPoint%22%3A%22%22%2C%22keyword%22%3A%22%22%7D&sort=0&pageSize=20&pageIndex=1',)
    def start_requests(self):
        cookies1s = self.f.readlines()  #按行读取,这里看一下type属性，好像是list？##########
        for cookies11 in cookies1s:
            cookies1_str = cookies11[0:-1].split('!')  ##["{'HttpOnly':'true','CNZZDATA1256274125':'449396278-1486362470-%7C1511061479','JSESSIONID':'B8D322E0130A505E8534D34F73C8B958','UM_distinctid':'15e7a03cd2123f-003758f8229392-1e2a3803-3d10d-15e7a03cd22279',}", '1,2']
            cookies1 = eval(cookies1_str[0])   #将字典样式的string ：{'HttpOnly':'true','CNZZDATA1256274125':'449396278-1486362470-%7C1511061479','JSESSIONID':'B8D322E0130A505E8534D34F73C8B958','UM_distinctid':'15e7a03cd2123f-003758f8229392-1e2a3803-3d10d-15e7a03cd22279',}  转换成字典,"eval"的作用
            goodlist = cookies11[0:-1].split('!')[1].split(',') ##这是商品的列表：['1', '2']
            yield scrapy.Request(url='http://mygifts.plateno.com/frontInterface/Shop_GetGoodsByCategory.do?categoryID=78&where=%7B%22startPoint%22%3A%22%22%2C%22endPoint%22%3A%22%22%2C%22keyword%22%3A%22%22%7D&sort=0&pageSize=20&pageIndex=1'+'#%s'%random.random(),callback=self.parse,meta={'goodlist':goodlist,'cookies1':cookies1},cookies=cookies1,dont_filter = True)
            ##dont_filter = True关闭scrapy的自动去重功能，使用与url相同，但是cookies变化的情况
    def parse(self,response):
        sites = json.loads(response.body_as_unicode()) ##使用scrapy解析json数据的时候，要使用这种格式，如果使用requests的话直接使用r.json()['']['']...格式
        goodslist = response.meta['goodlist']    ###将for循环写在start_requests，将来只能下goodslist中的第一单，是波涛服务器对一个账户的限制，账户下单的流程是单线程的，如果将for循环写在parse，将来只能下goodslist中的最后一单,因为波涛的服务器同时收到一个账号的两个处理请求，只会处理最后一个
        cookies1 = response.meta['cookies1']
        for ii in goodslist:
            i = int(ii)
            itemID = sites['result']['listInfo'][i]['itemID'] ##需要加入到商品详情页的请求中去，是变量
            #################这部分用于做商品详情页面中的筛选条件判断
            #goodsDetailpage = 'http://mygifts.plateno.com/frontInterface/Shop_GetGoodsByID.do?itemID=%s&categoryID=78'%itemID##商品详情页的json链接
            #r_detail = requests.get(goodsDetailpage,cookies=cookies1)
            #title = r_detail.json()['result']['itemName']  ###商品名
            #vipstock = r_detail.json()['result']['itemVIPStock'] ###vip可抢量额
            ################
            AddToCart = 'http://mygifts.plateno.com/frontInterface/Shop_AddGoodsToCart.do?itemID=%s&categoryID=78&itemStyle=0%%2C0&count=1&goodsType=0'%itemID  ###根据itemID将商品加入购物车
            r_addCart = requests.get(AddToCart,cookies=cookies1)
            ###############这部分中是改变cookies1，增加必须项
            cookie_list = r_addCart.cookies  ##requests方法中获取cookies的写法。print型如：<RequestsCookieJar[<Cookie cookie_cart182122378=a6f6ab288486a47238f33afa614ecd0085b21e1a72accdcff709a685900e2368f6945f81d6f45785 for mygifts.plateno.com/>, <Cookie HttpOnly=true for mygifts.plateno.com/frontInterface>]>
            for cl in cookie_list:
                #l_s = str(cl, encoding = "utf-8")  ##使用response.headers.getlist得到的列表里面的元素是bytle，需要转换成string才能做re匹配
                if(re.compile('cookie_cart').findall(cl.name)):  ##cl.name可以取出cookiejar里面的：cookie_cart182122378和HttpOnly
                    cookies1[cl.name] = cl.value
                else:
                    continue
            
            ###从这里开始使用自动捕获的cookie（cookies1已改变）
            order_page = 'http://mygifts.plateno.com/frontInterface/Shop_GetGoodsByCart.do?userID=0'##订单页的请求链接（qujiesuan）
            r_order = requests.get(order_page,cookies=cookies1)
            soup_order = BeautifulSoup(r_order.text,'lxml')
            #print(soup_order)
            
            token = r_order.json()['token'] ##用于支付页请求的子串
            pay_ok = 'http://mygifts.plateno.com/frontInterface/Shop_OrderSubmit.do?userID=0&couponId=-1&result=%%7B%%22addressID%%22%%3A%%22-1%%22%%2C%%22rowID%%22%%3A%%220%%2C%%22%%2C%%22remark%%22%%3A%%22%%22%%7D&token=%s'%token   ###确认付款页面的链接
            r_pay = requests.get(pay_ok,cookies=cookies1)

            ###############这部分中是改变cookies1，增加必须项
            cookie_list1 = r_pay.cookies  ##requests方法中获取cookies的写法。print型如：<RequestsCookieJar[<Cookie cookie_cart182122378=a6f6ab288486a47238f33afa614ecd0085b21e1a72accdcff709a685900e2368f6945f81d6f45785 for mygifts.plateno.com/>, <Cookie HttpOnly=true for mygifts.plateno.com/frontInterface>]>
            for cl1 in cookie_list1:
                #l_s = str(cl, encoding = "utf-8")  ##使用response.headers.getlist得到的列表里面的元素是bytle，需要转换成string才能做re匹配
                if(re.compile('cookie_cart').findall(cl1.name)):  ##cl.name可以取出cookiejar里面的：cookie_cart182122378和HttpOnly
                    cookies1[cl1.name] = cl1.value    
                elif(re.compile('cookie_gift').findall(cl1.name)):  ##这里当一次登录，有过下单记录的时候，会多出来一个cookie_gift，这个参数要加入到cookies1里面去，否则会重复下第一单的内容
                    cookies1[cl1.name] = cl1.value    
                else:
                    continue
            #soup_pay = BeautifulSoup(r_pay.text,'lxml') #调试使用
            orderNO = r_pay.json()['result'] ##用于“完成支付页面请求的子串”
            finish_page = 'http://mygifts.plateno.com/frontInterface/Shop_GetOrderByMoreOrderNo.do?userID=0&newOrderNo=%s'%orderNO   ##完成支付页面的链接
            r_finish = requests.get(finish_page,cookies=cookies1)
            soup_finish = BeautifulSoup(r_finish.text,'lxml') #调试使用

            #print (json.dumps(json.loads(soup_add.text),ensure_ascii=False))
            print('successssssssssssssssssss')
            print(cookies1)  
        



        