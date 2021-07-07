# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import scrapy
import csv
fp = open('G:\\学习\\数据采集\\数据采集大作业\\scrapy爬取去哪儿网\\qunar\\qunar7.csv', 'w+', newline='', encoding='utf8')
writer = csv.writer(fp)
writer.writerow(('城市', '价格', '出游人数', '评论数', '详细出游人数', '满意度', '来回交通工具', '行程天数', '住宿类型', '好评数', '目的地', '编号'))

class QunarPipeline:
    def process_item(self, item, spider):

        # try:
        writer.writerow((item['city'], item['prices'], item['tourists'], item['person_comments'], item['c_tourists'],
                         item['statisfaction'], item['transport'], item['travels_days'], item['accommodation'],
                         item['ratingExcellent'], item['destination'], item['number']))
        return item
        # except KeyError:
        #     pass


# 城市, 价格, 出游人数, 评论数, 详细出游人数, 满意度, 来回交通工具, 行程天数, 住宿类型, 行程内交通时长, 目的地, 编号
# City, price, tourist, person_comment, c_tourist,statisfactions,transports,attaction,accommodations,transport_times,destinations,numbers