from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

class School(Base):
    __tablename__ = 'school'

    cno = Column(Integer, primary_key=True)
    sno = Column(String(20))
    major = Column(String(20))
    grade = Column(String(6))
    sd = Column(String(40))

class Home(Base):
    __tablename__ = 'home'

    cno = Column(Integer, primary_key=True)
    province = Column(String(20))
    address = Column(String(30))
    tele = Column(String(12))

class Information(Base):
    __tablename__ = 'information'

    cno = Column(Integer, primary_key=True)
    pnum = Column(String(11))
    QQ = Column(String(10))
    wx = Column(String(20))
    email = Column(String(40))

class Person(Base):
    __tablename__ = 'person'

    NAME = Column(String(20))
    cno = Column(Integer, primary_key=True)
    age = Column(Integer)
    sex = Column(String(2))


# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/address_book')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()