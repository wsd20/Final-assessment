from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import re
import pandas as pd
import requests
import time
import threading
import random
from queue import Queue
import pymysql


df = pd.DataFrame()  # 设置一页爬取到的信息存储

# cookies信息
cookie_str = 'sessid=964936C8-9ED2-0CC4-2993-B38276237A36; aQQ_ajkguid=4D3757B2-EE82-5C90-25C5-E1C2A19314F6; lps=http%3A%2F%2Ffoshan.anjuke.com%2Fsale%2F%7C; ctid=24; twe=2; _stat_guid=0EC59070-63EA-47D7-9F4E-28DF3A2077A7; _prev_stat_guid=4D3757B2-EE82-5C90-25C5-E1C2A19314F6; _stat_rfpn=Aifang_Web_Loupan_View2_IndexPage; id58=e87rkF+Bn1Va05rVCk6nAg==; isp=true; cmctid=222; 58tj_uuid=930fff59-23eb-45aa-870b-7d82f455288f; new_session=0; init_refer=https%253A%252F%252Ffoshan.anjuke.com%252Fantispam-block%252F%253Ffrom%253Da…da9e8ff531ecf088c6a2a5064c95; xxzl_cid=8e12f24aac584018a6befd8c73b7670c; xzuid=04c005f8-9246-4086-855b-eab14373ce52; ajkAuthTicket=TT=e455f83c11d4065994cd82bea80b1215&TS=1602330514700&PBODY=HiUl8wuPUcy6ZkmtrDYfkTf-CkRsRnqilQJe-8ISFgiZ1lhABnYhnIeHKvo4NQuWpCsE64-a4bLGYH_MCOHPI4NbamJB1JknvL2kzLCZxIan0HMC_BLaJvebo8khMx9DyKQrCQbCrVka-aETxc84F6Ju_9qNoS1sb5AkDy_BRu4&VER=2; ajk_member_verify=8AtWWGTapTpg9vCgrfiXRWCBzEyQLirTjr66dVZfC10%3D; ajk_member_verify2=MjA0MDg5NjU3fHNpTEUycFZ8MQ%3D%3D; ajk_member_id=204089657'
cookies = {}
for i in cookie_str.split(";"):
    key,values = i.split("=",1)
    cookies[key] = values

href_queue = Queue()

c_tourists_queue = Queue()
statisfaction_queue = Queue()
transport_queue = Queue()
travels_days_queue = Queue()
attactions_queue = Queue()
accommodation_queue = Queue()
transport_time_queue = Queue()
destination_queue = Queue()
number_queue = Queue()


# 定义一个子类并重载 __init__()方法和 run()方法
class testThread(threading.Thread):
    def __init__(self,href_queue,city):
        # 初始化时调用基类的初始化函数 初始化基类
        threading.Thread.__init__(self)
        # 将参数赋值作为 self的属性 这样就可以将参数通过 self传递给 run方法
        self.href_queue = href_queue
        self.c_tourists_queue = c_tourists_queue
        self.statisfaction_queue = statisfaction_queue
        self.transport_queue = transport_queue
        self.travels_days_queue = travels_days_queue
        self.attactions_queue = attactions_queue
        self.accommodation_queue = accommodation_queue
        self.transport_time_queue = transport_time_queue
        self.destination_queue = destination_queue
        self.number_queue = number_queue
        self.city = city

    # 要在多线程里运行的函数
    def run(self):

        while not self.href_queue.empty():
            self.href = self.href_queue.get()

            ua = [
                'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36']
            headers = {'User-Agent': random.choice(ua)}

            # 设置ip代理池
            proxies = {
                'http': 'http://36.57.90.201:4226',
                'http': 'http://125.106.135.131:4276',
                'http': 'http://113.124.95.173:4234',
                'http': 'http://114.99.253.132:4235',
                'http': 'http://110.185.133.12:4224'
            }
            print('正在获取' + 'https:' + self.href)
            html = requests.get('https:'+self.href, headers=headers)
            # print(html.status_code)
            # print(html.text)
            time.sleep(0.2)
            # print(html.text)
            html.content.decode(encoding='utf-8')


            html_dom = etree.HTML(html.text, etree.HTMLParser(encoding='utf-8'))
            # release_time.append(html_dom.xpath('//*[@class="house-encode"]/span[2]/text()')[0])

            # if self.href[16:20] == 'tour' or self.href[16:21] == 'tours':
            try:
                self.c_tourists_queue.put(html_dom.xpath('//*[@class="resource-people"]/div[1]/a')[0].text)  # 详细出游人数
                self.statisfaction_queue.put(html_dom.xpath('//*[@class="resource-statisfaction-number"]')[0].text)  # 满意度

                self.transport_queue.put(html_dom.xpath('//*[@class="section-box-body"]/div[2]/div/div[4]/strong')[0].text)  # 来回交通工具     #返回两个（要改）
                self.travels_days_queue.put(html_dom.xpath('//*[@class="section-box-body"]/div[2]/div/div[1]/strong')[0].text)  # 行程天数  #返回两个（要改）
                self.attactions_queue.put(html_dom.xpath(
                    '//*[@id="J_Detail"]/div/div[4]/div[2]/div[4]/div[1]/div/div/div/div/div/div[1]/strong[1]')[0].text)  # 景点个数
                self.accommodation_queue.put(html_dom.xpath(
                    '//*[@id="J_Detail"]/div/div[4]/div[2]/div[4]/div[1]/div/div/div/div/div/div[3]/strong')[0].text)  # 住宿类型
                self.transport_time_queue.put(html_dom.xpath(
                    '//*[@id="J_Detail"]/div/div[4]/div[2]/div[4]/div[1]/div/div/div/div/div/div[4]/strong')[0].text)  # 行程内交通时长
                self.destination_queue.put(html_dom.xpath('//*[@id="J_Detail"]/div/div[3]/div[2]/div[2]/div/div[3]/strong')[0].text)  # 目的地
            except IndexError:
                self.transport_queue.put(' ')
                self.travels_days_queue.put(' ')
                self.c_tourists_queue.put(' ')  # 详细出游人数
                self.statisfaction_queue.put(' ')  # 满意度

                self.transport_queue.put(' ')  # 来回交通工具     #返回两个（要改）
                self.travels_days_queue.put(' ')  # 行程天数  #返回两个（要改）
                self.attactions_queue.put(' ')  # 景点个数
                self.accommodation_queue.put(' ')  # 住宿类型
                self.transport_time_queue.put(' ')  # 行程内交通时长
                self.destination_queue.put(' ')  # 目的地


# 创建线程
def threadstart(href_queue,city):
    # 用来存放线程的列表
    threads = []
    for i in range(12):
        # 像使用普通类一样
        t = testThread(href_queue,city)
        threads.append(t)

    # 开启所有线程
    for t in threads:
        time.sleep(0.4)
        t.start()

    # 阻塞主线程，直到所有线程全部完成
    for t in threads:
        t.join()



# 获取详细页信息
def get_detailinfo(prices,tourists,person_comments,number,city,hrefs):
    c_tourists = []
    statisfaction = []
    transport = []
    travels_days = []
    attactions = []
    accommodation = []
    transport_time = []
    destination = []

    infos_list = []

    Citys = [city]  # 设置城市列


    for i in range(len(hrefs)):
        href_queue.put(hrefs[i])

    threadstart(href_queue,city)

    for i in range(len(number)):
        c_tourists.append(c_tourists_queue.get())
        statisfaction.append(statisfaction_queue.get())
        transport.append(transport_queue.get())
        travels_days.append(travels_days_queue.get())
        attactions.append(attactions_queue.get())
        accommodation.append(accommodation_queue.get())
        transport_time.append(transport_time_queue.get())
        destination.append(destination_queue.get())



    Citys = [val for val in Citys for i in range(len(number))]  # 设置爬取到的二手房源的二手城市


    for City, price, tourist, person_comment, c_tourist,statisfactions,transports,attaction,accommodations,transport_times,destinations,numbers in zip(Citys, prices, tourists, person_comments, c_tourists,statisfaction,
                                                                 transport,attactions,accommodation,transport_time,destination,number):
        info = {
            '城市': City,
            '价格': price,
            '出游人数': tourist,
            '评论数': person_comment,
            '详细出游人数': c_tourist,
            '满意度': statisfactions,
            '来回交通工具': transports,
            '行程天数': attaction,
            '住宿类型': accommodations,
            '行程内交通时长': transport_times,
            '目的地': destinations,
            '编号': numbers
        }
        infos_list.append(info)


    df = pd.DataFrame({
        '城市':Citys,
        '价格': prices,
        '出游人数': tourists,
        '评论数': person_comments,
        '详细出游人数': c_tourists,
        '满意度': statisfaction,
        '来回交通工具': transport,
        '行程天数': attactions,
        '住宿类型': accommodation,
        '行程内交通时长': transport_time,
        '目的地': destination,
        '编号':number
    })
    return df,infos_list


# main函数
def main():
    # 网页驱动
    all_data = pd.DataFrame()  # 设置all_data用于整合数据一起存储
    driver = webdriver.Firefox()

    citys = ['广州']

    # https://www.tuniu.com/g700/whole-gz-0/list-h0?pcat=27
    # https://www.tuniu.com/g906/whole-gz-0/list-h0/13
    # https://www.tuniu.com/g200/whole-gz-0/list-h0?pcat=27
    # https://www.tuniu.com/g2702/whole-sh-0/list-h0?pcat=247
    # https://www.tuniu.com/g600/whole-sh-0/list-h0?pcat=27
    for city in citys:
        city_str = 'https://www.tuniu.com/g700/whole-gz-0/list-h0?pcat=27'
        driver.get(city_str)
        wait = WebDriverWait(driver, 45)
        time.sleep(6)

        # 从第2页开始
        page = 1

        # 当“下一页”按钮可以点击时继续
        while True:
            time.sleep(1)
            # 当下一页按钮可以点击的时候开始爬取
            wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR,'#contentcontainer > div.content_bottom > div.main.fl > div.main-content > div.pagination > div > a.page-next')
            ))
            print('第' + str(page) + '页')

            # 开始爬取
            wait = WebDriverWait(driver, 16)

            dom = etree.HTML(driver.page_source, etree.HTMLParser(encoding="utf-8"))

            prices = dom.xpath('//ul/li/div/a/div[2]/div[2]/div[1]/em')  # 价格
            tourists = dom.xpath('//ul/li/div/a/div[2]/div[2]/div[2]/div[2]/p[1]/i')  # 出游人数
            person_comments = re.findall('<p class="person-comment"><i>(.*?)</i>点评</p>',driver.page_source,re.S|re.M)  # 评论数
            # person_comments = dom.xpath('//ul/li/div/a/div[2]/div[2]/div[2]/div[2]/p[2]/i')  # 评论数

            # 获取详细页网址，进入到详细页爬取
            hrefs = dom.xpath('//*[@id="contentcontainer"]/div[2]/div[1]/div[1]/div[1]/ul/li/div/a/@href')  # 详细页网址
            number = []

            for href in hrefs:
                number.append(re.findall('//www.tuniu.com/.*?/(\d*)',href)[0])


            while len(prices) < 30:
                prices.append(' ')
            while len(tourists) < 30:
                tourists.append(' ')
            while len(person_comments) < 30:
                person_comments.append(' ')


                # if len(person_comments) < 30:
                #     person_comments.append(' ')
                # if len(prices) < 30:
                #     prices.append(' ')
                # if len(tourists) < 30:
                #     person_comments.append(' ')

            for i in range(len(prices)):
                if type(prices[i]) != str:
                    prices[i] = prices[i].text


            for i in range(len(tourists)):
                if type(tourists[i]) != str:
                    tourists[i] = tourists[i].text

            # print(len(prices))
            # print(prices)
            # print(len(tourists))
            # print(tourists)

            Citys = [city]  # 设置城市列

            # 执行到一半时会爬取不到数据，重复执行，直到成功获取到所有数据
            try:
                df,infos_list = get_detailinfo(prices,tourists,person_comments,number, city,hrefs)
            except IndexError and ValueError:
                df,infos_list = get_detailinfo(prices,tourists,person_comments,number, city,hrefs)
            finally:
                df,infos_list = get_detailinfo(prices,tourists,person_comments,number, city, hrefs)

            print(df)
            all_data = pd.concat([all_data, df], axis=0)  # 将每一页爬取到数据拼接到一块

            MySQL(infos_list)

            # 判断下一页可不可以点击
            if (driver.find_elements_by_css_selector('#contentcontainer > div.content_bottom > div.main.fl > div.main-content > div.pagination > div > a.page-next')) == []:
                break

            confirm_btn = wait.until(  # 定位“后页”
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,'#contentcontainer > div.content_bottom > div.main.fl > div.main-content > div.pagination > div > a.page-next')
                ))
            confirm_btn.click()  # 单击“后页”进行翻页
            page = page + 1
            if page > 17:
                break

    all_data.to_csv('./tuniu6.csv')
    driver.close()


# 与MySQL建立连接，并把数据wsd数据库中存储到tuniu表中
def MySQL(info_list):
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='wsd', port=3305,
                           charset='utf8')  # 与 MySQL服务器建立连接
    cursor = conn.cursor()  # 创建游标对象
    # for info in info_list:
    #     print(info)
    for infos in info_list:
        infos_list = []
        for info in infos.keys():
            infos_list.append(infos[info])
        cursor.execute("insert into tuniu2(城市, 价格, 出游人数, 评论数, 详细出游人数, 满意度, 来回交通工具, 行程天数, 住宿类型, 行程内交通时长, 目的地, 编号)"
                       "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", infos_list)
        conn.commit()  # 提交事务


# 调用main函数
if __name__ == '__main__':
    main()


