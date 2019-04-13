# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
def _utf8_to_gbk(string):
    if string is not str:
        string = str(string)
    return string.encode('gbk',errors='ignore').decode('gbk')


def oracle_field():
    """
    去掉 \n \r\ t与空格，再把utf8转成gbk
    :return:
    """
    return scrapy.Field(
            input_processor=MapCompose(_utf8_to_gbk),
        output_processor=TakeFirst()
    )

class DiseaseItem(scrapy.Item):
    name = oracle_field()
    overview = oracle_field()
    othername = oracle_field()
    medicare = oracle_field()
    infection = oracle_field()
    cure = oracle_field()
    cure_rate = oracle_field()
    cure_period = oracle_field()
    infection_people = oracle_field()
    fee = oracle_field()
    relate_disease =  oracle_field()
    # disease_type = oracle_field()


class ZhengzhuangItem(scrapy.Item):
    name = oracle_field()
    overview = oracle_field()
    similar = oracle_field()
    reason = oracle_field()
    howprepare = oracle_field()
    knowledge = oracle_field()


class BuweiItem(scrapy.Item):
    name = oracle_field()
    son_buwei_name = oracle_field()
    url =  oracle_field()


class KeshiItem(scrapy.Item):
    name = oracle_field()
    son_keshi_name = oracle_field()
    url =  oracle_field()


class keshi_zhengzhuang(scrapy.Item):
    son_keshi_name = oracle_field()
    fzhengzhuangname = oracle_field()


class buwei_zhengzhuang(scrapy.Item):
    son_buwei_name = oracle_field()
    fzhengzhuangname = oracle_field()


class check_zhengzhuang(scrapy.Item):
    fcheckname = oracle_field()
    fzhengzhuangname = oracle_field()


class keshi_disease(scrapy.Item):
    son_keshi_name = oracle_field()
    fdiseasename = oracle_field()


class buwei_disease(scrapy.Item):
    son_buwei_name = oracle_field()
    fdiseasename = oracle_field()


class disease_zhengzhuang(scrapy.Item):
    # 定义各字段
    fdiseasename = oracle_field()
    fzhengzhuangname = oracle_field()

class check_disease(scrapy.Item):
    fcheckname = oracle_field()
    fdiseasename = oracle_field()