# This package will contain the spiders of your Scrapy project
import re
from .. import items
from scrapy import Request, Spider
from ..createTable import *
from ..settings import SA_CONN
from sqlalchemy import select

# Please refer to the documentation for information on how to create and manage
# your spiders.
class KeshiSpider(Spider):

    name = "KeshiSpider"
    host = "http://jbk.39.net"

    def start_requests(self):
        start_url = "http://jbk.39.net/bw/"
        h = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        yield Request(url=start_url, headers=h)

    def parse(self, response):
        keshi_list = response.xpath("//div[@class='lookup_department lookup_cur']/div/ul/li/a")
        yield from self._yield_request(keshi_list)

    def _yield_request(self, keshi_list):
        for keshi in keshi_list:
            keshi_name = keshi.xpath("./text()").extract()[0]
            url = keshi.xpath("./@href").extract()[0]
            url = self.host + url
            h = {
                'Host': 'jbk.39.net',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
            }
            yield Request(url=url, headers=h, callback=self.parse_detail, meta={"name": keshi_name})

    def parse_detail(self, response):
        second_keshe_list = response.xpath("//ul[@class='type_subscreen_unit']/li/a")
        if not second_keshe_list:
            keshi_item = items.KeshiItem()
            keshi_item["url"] = response.url
            keshi_item["son_keshi_name"] = response.meta["name"]
            keshi_item["name"] = response.meta["name"]
            yield keshi_item

        for second_keshe in second_keshe_list:
            keshi_item = items.KeshiItem()
            keshi_item["url"] = self.host + second_keshe.xpath("@href").extract()[0]
            keshi_item["son_keshi_name"] = second_keshe.xpath("text()").extract()[0]
            keshi_item["name"] = response.meta["name"]
            yield keshi_item

class BuweiSpider(KeshiSpider):

    name = "BuweiSpider"
    host = "http://jbk.39.net"

    def parse(self, response):
        keshi_list = response.xpath("//div[@class='lookup_position ']/div/ul/li/a")
        yield from self._yield_request(keshi_list)

    def parse_detail(self, response):
        second_keshe_list = response.xpath("//ul[@class='type_subscreen_unit']/li/a")
        if not second_keshe_list:
            keshi_item = items.BuweiItem()
            keshi_item["url"] = response.url
            keshi_item["son_buwei_name"] = response.meta["name"]
            keshi_item["name"] = response.meta["name"]
            yield keshi_item

        for second_keshe in second_keshe_list:
            keshi_item = items.BuweiItem()
            keshi_item["url"] = self.host + second_keshe.xpath("@href").extract()[0]
            keshi_item["son_buwei_name"] = second_keshe.xpath("text()").extract()[0]
            keshi_item["name"] = response.meta["name"]
            yield keshi_item

class ZhengzhuangSipder(Spider):

    name = "ZhengzhuangSipder"
    host = "http://jbk.39.net"
    engine = create_engine(SA_CONN, echo=True)
    conn = engine.connect()
    h = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }

    def get_keshi_url(self):
        keshi_t = keshi.__table__
        sql = select([keshi_t.c.son_keshi_name, keshi_t.c.url])
        return self.conn.execute(sql).fetchall()

    def get_buwei_url(self):
        buwei_t = buwei.__table__
        sql = select([buwei_t.c.son_keshi_name, buwei_t.c.url])
        return self.conn.execute(sql).fetchall()

    def start_requests(self):
        ks = self.get_keshi_url()

        for name, url in ks:
            yield from self._start_requests(name, url, "keshi")

    def _start_requests(self, keshi_name, url, table_name):
        h = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        meta = {}
        meta["table_name"] = table_name
        meta["name"] = keshi_name
        yield Request(url=url[:-1] + "_t2_p1", headers=h, meta=meta)

    def parse(self, response):
        """
        0.get zhengzhuang url from page
        1.add relation in keshi_zhengzhuang and buwei_zhengzhuang
        2.yield request
        3. page + 1
        """
        table_name = response.meta["table_name"]

        zhengzhuang_list = response.xpath("//div[@class='result_content']/div/div/p[1]/a")
        for zhengzhuang in zhengzhuang_list:
            item = getattr(items, table_name + "_zhengzhuang")()
            zhengzhuangname = zhengzhuang.xpath("text()").extract()[0]
            url = zhengzhuang.xpath("@href").extract()[0]

            item["fzhengzhuangname"] = zhengzhuangname
            item["son_" + table_name + "_name"] = response.meta["name"]
            yield item
            yield Request(url=url, headers=self.h, meta={"name": zhengzhuangname}, callback=self.parse_zhengzhuang_page)
            yield from self.__next_page(response)

    def __next_page(self, response):
        if self.__stop_next_page(response):
            try:
                num = str(int(re.search("_p(\d+)", response.url).group(1)) + 1)
            except AttributeError:
                print(response.url)
            url = re.sub("_p(\d+)", "_p"+num, response.url)
            meta = {}
            meta.update({"name": response.meta["name"]})
            meta.update({"table_name": response.meta["table_name"]})
            yield Request(url=url, headers=self.h,callback=self.parse, meta=response.meta)

    def __stop_next_page(self, response):
        if "暂时没有" in response.xpath("//div[@class='result_content']")[0].xpath("string(.)").extract():
            return False
        else:
            return True

    def parse_zhengzhuang_page(self, response):
        """
        0.get zhengzhuang cols from page
        1.add relation in check_zhengzhuang
        2.fill zhengzhuang cols
        """
        item = items.ZhengzhuangItem()
        item["name"] = response.meta["name"]
        try:
            tmp = response.xpath("//p[@class='sort2']")
            item["overview"] =  items._utf8_to_gbk(tmp[0].xpath("string(.)").extract()[0])
        except Exception as e:
            print("parse_zhengzhuang_page overview" + str(e))

        try:
            disease_list = response.xpath("//table[@class='dis']//tr/td[1]/a/@title").extract()
            for disease_name in disease_list:
                disease_zhengzhuang_item =items.disease_zhengzhuang()
                disease_zhengzhuang_item["fdiseasename"] = disease_name
                disease_zhengzhuang_item["fzhengzhuangname"] = response.meta["name"]
                yield disease_zhengzhuang_item
        except Exception as e:
            print("parse_zhengzhuang_page disease_bingzheng" + str(e))
        yield Request(url=response.url + "zzqy",
                      meta={"item": item, "url": response.url}, callback=self.zzqy)

    def zzqy(self, response):
        """
        症状起因
        """
        item = response.meta["item"]
        item["reason"] =  items._utf8_to_gbk(response.xpath("//div[@class='lbox_con']")[0].xpath("string(.)").extract()[0])
        yield Request(url=response.meta["url"] + "zdxs",
                      meta={"item": item, "url": response.meta["url"]}, callback=self.zdxs)

    def zdxs(self, response):
        """
        诊断详情
        """
        item = response.meta["item"]
        item["howprepare"] =  items._utf8_to_gbk(response.xpath("//div[@class='lbox_con']")[0].xpath("string(.)").extract()[0])
        yield Request(url=response.meta["url"] + "jcjb",
                      meta={"item": item, "url": response.meta["url"]}, callback=self.jcjb)

    def jcjb(self, response):
        """
        检查鉴别
        """
        item = response.meta["item"]
        item["similar"] =  items._utf8_to_gbk(",".join(response.xpath("//ul[@class='list_kind']/li/dl/dt/@title").extract()))
        try:
            for jc_name in response.xpath("//div[@class='checkbox-data']/table/tbody/tr/td[1]/a/text()").extract():
                check_item = items.check_zhengzhuang()
                check_item["fcheckname"] = jc_name
                check_item["fzhengzhuangname"] = item["name"]
                yield check_item
        except Exception as e:
            print("jcjb" + str(e))
        yield Request(url=response.meta["url"] + "jzzn",
                      meta={"item": item, "url": response.meta["url"]}, callback=self.jzzn)

    def jzzn(self, response):
        """
        就诊指南
        """
        item = response.meta["item"]
        try:
            item["knowledge"] =  items._utf8_to_gbk(response.xpath("//div[@class='zn-top clearfix']")[0].xpath("string(.)").extract())
        except Exception as e:
            print("jzzn"+str(e))
        yield item

class DiseaseSipder(ZhengzhuangSipder):

    name = "DiseaseSipder"
    host = "http://jbk.39.net"
    engine = create_engine(SA_CONN, echo=True)
    conn = engine.connect()
    h = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }

    def _start_requests(self, keshi_name, url, table_name):
        h = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        meta = {}
        meta["table_name"] = table_name
        meta["name"] = keshi_name
        yield Request(url=url[:-1] + "_t1_p1", headers=h, meta=meta)

    def parse(self, response):
        """
        0.get zhengzhuang url from page
        1.add relation in keshi_zhengzhuang and buwei_zhengzhuang
        2.yield request
        3. page + 1
        """
        table_name = response.meta["table_name"]

        disease_list = response.xpath("//div[@class='result_content']/div/div/p[1]/a")
        for disease in disease_list:
            item = getattr(items, table_name + "_disease")()
            diseasename = disease.xpath("text()").extract()[0]
            url = disease.xpath("@href").extract()[0]

            item["fdiseasename"] = diseasename
            item["son_" + table_name + "_name"] = response.meta["name"]
            yield item
            yield Request(url=url, headers=self.h, meta={"name": diseasename}, callback=self.parse_disease_page)
            yield from self.__next_page(response)

    def parse_disease_page(self, response):
        item = items.DiseaseItem()
        selector = response.xpath("//ul[@class='information_ul']")[0]
        item["name"] = response.meta["name"]
        item["overview"] = items._utf8_to_gbk(response.xpath("//p[@class='information_l']/text()").extract()[0])
        item["othername"] = self.__taker_first(selector.xpath("./li[contains(./i/text(), '别名')]/span"))
        item["medicare"] = self.__taker_first(selector.xpath("./li[contains(./i/text(), '是否医保')]/span"))
        item["infection"] = self.__taker_first(selector.xpath("./li[contains(./i/text(), '传染性')]/span"))
        item["cure"] = self.__taker_first(selector.xpath("./li[contains(./i/text(), '治疗方法')]/span"))
        item["cure_rate"] = self.__taker_first(selector.xpath("./li[contains(./i/text(), '治愈率')]/span"))
        item["cure_period"] = self.__taker_first(selector.xpath("./li[contains(./i/text(), '治疗周期')]/span"))
        item["infection_people"] = self.__taker_first(selector.xpath("./li[contains(./i/text(), '多发人群')]/span"))
        item["fee"] = self.__taker_first(selector.xpath("./li[contains(./i/text(), '治疗费用')]/span"))
        item["relate_disease"] = self.__taker_first(selector.xpath("./li[contains(./i/text(), '并发症')]/span"))
        # item["disease_type"] = response.xpath("./li[contains(./i/text(), '别名')]/span/text()").extract()
        yield item

        item = items.check_disease()
        for jc_name in selector.xpath("./li[contains(./i/text(), '临床检查')]/span/a/text()").extract():
            item["fcheckname"] = jc_name
            item["fdiseasename"] = response.meta["name"]
            yield item

    def __taker_first(self, l):
        if l:
            result = l[0].xpath("string(.)").extract()
            if isinstance(result, list):
                result = result[0]
            return items._utf8_to_gbk(result)
        else: return ""

    def __next_page(self, response):
        if self.__stop_next_page(response):
            try:
                num = str(int(re.search("_p(\d+)", response.url).group(1)) + 1)
            except AttributeError:
                print(response.url)
            url = re.sub("_p(\d+)", "_p"+num, response.url)
            meta = {}
            meta.update({"name": response.meta["name"]})
            meta.update({"table_name": response.meta["table_name"]})
            yield Request(url=url, headers=self.h,callback=self.parse, meta=response.meta)

    def __stop_next_page(self, response):
        if "暂时没有" in response.xpath("//div[@class='result_content']")[0].xpath("string(.)").extract():
            return False
        else:
            return True

class BuweiRelate(Spider):

    name = "BuweiRelateSipder"
    host = "http://jbk.39.net"
    engine = create_engine(SA_CONN, echo=True)
    conn = engine.connect()
    h = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }

    def get_buwei_url(self):
        buwei_t = buwei.__table__
        sql = select([buwei_t.c.son_buwei_name, buwei_t.c.url])
        return self.conn.execute(sql).fetchall()

    def start_requests(self):
        bw = self.get_buwei_url()
        for name, url in bw:
            yield from self._start_requests(name, url, "buwei")

    def _start_requests(self, keshi_name, url, table_name):
        h = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        meta = {}
        meta["table_name"] = table_name
        meta["name"] = keshi_name
        meta["elem"] = "disease"
        yield Request(url=url[:-1] + "_t1_p1", headers=h, meta=meta)
        meta["elem"] = "zhengzhuang"
        yield Request(url=url[:-1] + "_t2_p1", headers=h, meta=meta)

    def parse(self, response):
        """
        0.get zhengzhuang url from page
        1.add relation in keshi_zhengzhuang and buwei_zhengzhuang
        2.yield request
        3. page + 1
        """
        table_name = response.meta["table_name"]

        elem_list = response.xpath("//div[@class='result_content']/div/div/p[1]/a")
        for elem in elem_list:
            item = getattr(items, table_name + "_" + response.meta["elem"])()
            elemname = elem.xpath("text()").extract()[0]
            url = elem.xpath("@href").extract()[0]

            item[f"f{response.meta['elem']}name"] = elemname
            item["son_" + table_name + "_name"] = response.meta["name"]
            yield item
            yield from self.__next_page(response)

    def __next_page(self, response):
        if self.__stop_next_page(response):
            try:
                num = str(int(re.search("_p(\d+)", response.url).group(1)) + 1)
            except AttributeError:
                print(response.url)
            url = re.sub("_p(\d+)", "_p" + num, response.url)
            meta = {}
            meta.update({"name": response.meta["name"]})
            meta.update({"table_name": response.meta["table_name"]})
            yield Request(url=url, headers=self.h, callback=self.parse, meta=response.meta)

    def __stop_next_page(self, response):
        if "暂时没有" in response.xpath("//div[@class='result_content']")[0].xpath("string(.)").extract():
            return False
        else:
            return True

