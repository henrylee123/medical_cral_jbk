# -*- coding: utf-8 -*-
import re
from .createTable import *
from sqlalchemy import create_engine
import cx_Oracle
from sqlalchemy import exc
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class MedicalCralJbkPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            conn=crawler.settings.get('SA_CONN'))

    def __init__(self, conn):
        # 连接数据库
        engine = create_engine(conn, echo=False)
        # # 绑定引擎
        # metadata = MetaData(engine)
        # 连接数据表
        class InsertObject():
            KeshiItem = keshi.__table__.insert()
            BuweiItem = buwei.__table__.insert()
            DiseaseItem = disease.__table__.insert()
            ZhengzhuangItem = zhengzhuang.__table__.insert()
            keshi_disease = keshi_disease.__table__.insert()
            keshi_zhengzhuang = keshi_zhengzhuang.__table__.insert()
            buwei_disease = buwei_disease.__table__.insert()
            buwei_zhengzhuang = buwei_zhengzhuang.__table__.insert()
            check_zhengzhuang = check_zhengzhuang.__table__.insert()
            check_disease = check_disease.__table__.insert()
            disease_zhengzhuang = disease_zhengzhuang.__table__.insert()

        self.inso = InsertObject
        self.conn = engine.connect()

    def process_item(self, item, spider):
        d = dict(item)
        # 得到表名
        table_name  = re.search("\.([^\.]+)'", str(type(item))).group(1)
        # 绑定要插入的数据
        ins = getattr(self.inso, table_name).values(**d)
        # 执行语句
        try:
            result = self.conn.execute(ins)
        except cx_Oracle.IntegrityError:
            print("cx_Oracle.IntegrityError: " + table_name)
        except exc.IntegrityError:
            print("exc.IntegrityError: " + table_name)
        return item
