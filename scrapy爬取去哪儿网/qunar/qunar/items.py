# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QunarItem(scrapy.Item):
    # define the fields for your item here like:
    city =  scrapy.Field()                   # 城市

    prices = scrapy.Field()                   # 价格
    tourists = scrapy.Field()                 # 出游人数
    person_comments = scrapy.Field()          # 评论数

    hrefs = scrapy.Field()                    # 详细页网址

    c_tourists = scrapy.Field()               # 详细出游人数
    statisfaction = scrapy.Field()            # 满意度
    transport = scrapy.Field()                # 来回交通工具
    travels_days = scrapy.Field()             # 行程天数
    accommodation = scrapy.Field()            # 住宿类型

    ratingExcellent = scrapy.Field()          # 好评数 (待行程内交通时长)
    destination = scrapy.Field()              # 目的地
    number = scrapy.Field()                   # 编号


# 城市, 价格, 出游人数, 评论数, 详细出游人数, 满意度, 来回交通工具, 行程天数, 住宿类型, 行程内交通时长, 目的地, 编号
# City, price, tourist, person_comment, c_tourist,statisfactions,transports,attaction,accommodations,transport_times,destinations,numbers