import scrapy
from scrapy.selector import Selector
from qunar.items import QunarItem
import re
import json
# from scrapy.http import Request
import time


class QunarspiderSpider(scrapy.Spider):
    name = 'qunarspider'
    # allowed_domains = ['tuan.qunar.com']
    start_urls = ['https://tuan.qunar.com/vc/index.php?category=travel_d&limit={}%2C30'.format(str(i)) for i in range(3000,6000,30)]
# https://tuan.qunar.com/vc/index.php?category=all&limit={}%2C30&function=%E8%B7%9F%E5%9B%A2%E6%B8%B8
    # https://tuan.qunar.com/vc/index.php?category=travel_d&limit=30%2C30
#https://tuan.qunar.com/vc/index.php?category=all&function=%E8%B7%9F%E5%9B%A2%E6%B8%B8&limit=6000%2C30
    # start_urls = ['https://tuan.qunar.com/vc/index.php?category=all&limit=0%2C30']


    # 主页爬取
    def parse(self, response):
        item = QunarItem()
        html  = str(response.body.decode('utf-8'))

        # print(html)

        try:
            urls = re.findall(r'(//dujia.qunar.com/pi/detail_\d*)\?',html)          # 详细页网址
            tourists = re.findall(r'<em>(\d*)</em>人已购</span>', html, re.S)  # 出游人数
            prices = re.findall(r'\"cash.*?\">¥</b><em>(.*?)</em></span>', html, re.S | re.M)  # 价格

            i = 0
            for url_2 in urls:
                item['tourists'] = tourists[i]
                item['prices'] = prices[i]
                item['c_tourists'] = tourists[i]

                i +=1

                yield scrapy.Request(
                    'https:' + url_2,
                    callback=self.parse_mid,
                    meta={"url_2":url_2,"item":item},
                    dont_filter=True

                )

        except IndexError:
            pass


        for url_1 in self.start_urls:
            yield scrapy.Request(
                url_1,
                callback=self.parse,

            )


    def parse_mid(self,response):
        url_2 = response.meta['url_2']
        item = response.meta['item']

        try:
            selector2 = Selector(response)  # 使用selector对请求返回的响应
            html = str(response.body.decode('utf-8'))
            # print(html)

            url = re.findall(r"ocation.href = '(//.*\.package.qunar.com/user/detail.jsp\?id=\d*)", html,re.S | re.M)[0]  # 详细页网址

            yield scrapy.Request(
                "https:" + url,
                callback=self.parse_detail,
                meta={"url_2": url_2, "item": item},

            )
        except IndexError:
            item['statisfaction'] = ' '
            item['transport'] = ' '
            item['travels_days'] = ' '
            item['accommodation'] = ' '
            item['destination'] = ' '
            item['number'] = ' '
            item['city'] = ' '
            item['person_comments'] = ' '
            item['ratingExcellent'] = ' '
            yield item


    # 详细页爬取
    def parse_detail(self,response):

        url_2 = response.meta['url_2']
        item = response.meta['item']

        url_3 = 'https://hqsr1.package.qunar.com/user/comment/product/queryComments.json'

        selector2 = Selector(response)  # 使用selector对请求返回的响应
        html = str(response.body.decode('utf-8'))
        # print(html)


        try:
            statisfaction = re.findall(r'<var class="js-shop-satisfaction">(.*?)</var>', html, re.S | re.M)  # 满意度
            transport = re.findall(r'<a href="javascript:;" jumpto="ss-traffics" class="js-click-anchor">(.*?)</a></em>', html, re.S | re.M)  # 来回交通工具
            travels_days = re.findall(r'<em>(.天.*?)</em>', html, re.S | re.M)  # 行程天数
            accommodation = re.findall(r'jumpto="ss-hotel-infos"  class="js-click-anchor">(.*?)</a></em>', html, re.S | re.M)  # 住宿类型
            destination = re.findall('<span class="basic-info">.*?<em>(.*?)</em>', html, re.S | re.M)  # 目的地
            number = re.findall('<label>产品编号</label>.*?<span>(.*?)</span>', html, re.S | re.M)  # 编号
            city = re.findall('<em class="deptCity">(.*?)</em>', html, re.S | re.M)

            print(statisfaction)
            print(transport)
            print(travels_days)
            print(accommodation)
            print(destination)
            print(number)
            print(city)



            if len(statisfaction) >0:
                item['statisfaction'] = statisfaction[0]
            else:
                item['statisfaction'] = ' '

            if len(transport) >0:
                item['transport'] = transport[0]
            else:
                item['transport'] = ' '

            if len(travels_days) >0:
                item['travels_days'] = travels_days[0]
            else:
                item['travels_days'] = ' '

            if len(accommodation) >0:
                item['accommodation'] = accommodation[0]
            else:
                item['accommodation'] = ' '

            if len(destination) >0:
                item['destination'] = destination[0]
            else:
                item['destination'] = ' '

            if len(number) >0:
                item['number'] = number[0]
            else:
                item['number'] = ' '


            if len(city) >0:
                item['city'] = city[0]
            else:
                item['city'] = ' '



            Myformdata = {'type': 'all',
                      'pageNo': '1',
                      'pageSize': '10',
                      'productId': number[0],
                      'rateStatus': 'ALL'}


            # if item['number'] == []:
            #     yield scrapy.FormRequest(
            #         url_3,
            #         callback=self.parse_detail,
            #         meta={"item": item},
            #         dont_filter=True
            #     )


            yield scrapy.FormRequest(
                url_3,
                callback=self.parse_detail_2,
                meta={"item": item},
                formdata = Myformdata,
                dont_filter = True
            )

        except IndexError:
            pass






    # 动态加载内容爬取
    def parse_detail_2(self,response):
        # item = IthomeItem()  # 生成一个item对象 包括8个成员变量
        item = response.meta['item']
        json_data = json.loads(response.text)
        print(json_data)

        try:
            item['person_comments'] = json_data['data']['totalComment']  # 评论数
            item['ratingExcellent'] = json_data['data']['ratingExcellent']  # 好评数

            print(item['person_comments'])
            print(item['ratingExcellent'])

        except IndexError:
            pass

        yield item


