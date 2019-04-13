import sqlalchemy as sa, uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, func
if __name__ == "__main__":
    from settings import SA_CONN
else:
    from .settings import SA_CONN
__Base = declarative_base()
__engine = create_engine(SA_CONN, echo=True)

def _guid():
    return uuid.uuid4().hex


# ***************主表*******************
class __origin():
    fid = sa.Column(sa.String(40), primary_key=True, default=_guid)
    name = sa.Column(sa.String(500))
    udtime = sa.Column(sa.Date, server_default = func.now())
    isuse = sa.Column(sa.String(10))


class zhengzhuang(__Base, __origin):
    __tablename__ = 'zhengzhuang'
    # 定义各字段
    overview = sa.Column(sa.String(3000))
    disease = sa.Column(sa.String(2000))
    similar = sa.Column(sa.String(2000))
    reason = sa.Column(sa.CLOB)
    checkway = sa.Column(sa.String(2000))
    howprepare = sa.Column(sa.CLOB)
    knowledge = sa.Column(sa.CLOB)


class disease(__Base, __origin):
    __tablename__ = 'disease'
    # 定义各字段
    overview = sa.Column(sa.String(4000))
    othername = sa.Column(sa.String(500))
    medicare = sa.Column(sa.String(200))
    infection = sa.Column(sa.String(200))
    cure = sa.Column(sa.String(500))
    cure_rate = sa.Column(sa.String(500))
    cure_period = sa.Column(sa.String(500))
    infection_people = sa.Column(sa.String(500))
    fee = sa.Column(sa.String(500))
    relate_disease =  sa.Column(sa.String(500))
    disease_type = sa.Column(sa.String(500))
#
#
# class jiancha(Base):
#     __tablename__ = 'disease'
#     # 定义各字段
#     fIdxId = sa.Column(sa.String(200))
#     fCrawlId = sa.Column(sa.String(200))
#     fAreaNm = sa.Column(sa.String(200))
#     fKeyword = sa.Column(sa.String(200))
#     fIdxDtKey = sa.Column(sa.String(200))
#     fIdxVal = sa.Column(sa.Numeric(16, 4))
#     fIdxDt = sa.Column(sa.Date)
#     fCreateDt = sa.Column(sa.Date)
#     fLastUpdDt = sa.Column(sa.Date)


# class shoushu(Base):
#     __tablename__ = 'disease'
#     # 定义各字段
#     fIdxId = sa.Column(sa.String(200))
#     fCrawlId = sa.Column(sa.String(200))
#     fAreaNm = sa.Column(sa.String(200))
#     fKeyword = sa.Column(sa.String(200))
#     fIdxDtKey = sa.Column(sa.String(200))
#     fIdxVal = sa.Column(sa.Numeric(16, 4))
#     fIdxDt = sa.Column(sa.Date)
#     fCreateDt = sa.Column(sa.Date)
#     fLastUpdDt = sa.Column(sa.Date)


class keshi(__Base, __origin):
    __tablename__ = 'keshi'
    # 定义各字段
    son_keshi_id = sa.Column(sa.String(40), default=_guid)
    son_keshi_name = sa.Column(sa.String(500))
    url =  sa.Column(sa.String(300))

class buwei(__Base, __origin):
    __tablename__ = 'buwei'
    # 定义各字段
    son_buwei_id = sa.Column(sa.String(40), default=_guid)
    son_buwei_name = sa.Column(sa.String(500))
    url =  sa.Column(sa.String(300))


# ***************关系表*******************

class keshi_zhengzhuang(__Base, __origin):
    __tablename__ = 'keshi_zhengzhuang'
    # 定义各字段
    son_keshi_id = sa.Column(sa.String(40))
    son_keshi_name = sa.Column(sa.String(500))
    fzhengzhuangid = sa.Column(sa.String(40))
    fzhengzhuangname = sa.Column(sa.String(500))


class keshi_disease(__Base, __origin):
    __tablename__ = 'keshi_disease'
    # 定义各字段
    son_keshi_id = sa.Column(sa.String(40))
    son_keshi_name = sa.Column(sa.String(500))
    fdiseaseid = sa.Column(sa.String(40))
    fdiseasename = sa.Column(sa.String(500))

class buwei_disease(__Base, __origin):
    __tablename__ = 'buwei_disease'
    # 定义各字段
    son_buwei_id = sa.Column(sa.String(40))
    son_buwei_name = sa.Column(sa.String(500))
    fdiseaseid = sa.Column(sa.String(40))
    fdiseasename = sa.Column(sa.String(500))

class buwei_zhengzhuang(__Base, __origin):
    __tablename__ = 'buwei_zhengzhuang'
    # 定义各字段
    son_buwei_id = sa.Column(sa.String(40))
    son_buwei_name = sa.Column(sa.String(500))
    fzhengzhuangid = sa.Column(sa.String(40))
    fzhengzhuangname = sa.Column(sa.String(500))


class check_zhengzhuang(__Base, __origin):
    __tablename__ = 'check_zhengzhuang'
    # 定义各字段
    fcheckid = sa.Column(sa.String(40))
    fcheckname = sa.Column(sa.String(500))
    fzhengzhuangid = sa.Column(sa.String(40))
    fzhengzhuangname = sa.Column(sa.String(500))


class check_disease(__Base, __origin):
    __tablename__ = 'check_disease'
    # 定义各字段
    fcheckid = sa.Column(sa.String(40))
    fcheckname = sa.Column(sa.String(500))
    fdiseaseid = sa.Column(sa.String(40))
    fdiseasename = sa.Column(sa.String(500))


class disease_zhengzhuang(__Base, __origin):
    __tablename__ = 'disease_zhengzhuang'
    # 定义各字段
    fdiseaseid = sa.Column(sa.String(40))
    fdiseasename = sa.Column(sa.String(500))
    fzhengzhuangid = sa.Column(sa.String(40))
    fzhengzhuangname = sa.Column(sa.String(500))


if __name__ == "__main__":
    __Base.metadata.create_all(__engine)