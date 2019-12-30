from sqlalchemy import Column, Text, DateTime, String, Integer, Float, ForeignKey, create_engine, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:123456@127.0.0.1:5433/bookstore')

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    uid = Column(Text, primary_key=True)
    login_pwd = Column(Text)
    terminal = Column(Text)
    token = Column(Integer)
    pay_pwd = Column(Text)
    money = Column(Float)

class Store(Base):
    __tablename__ = 'store'
    sid = Column(Text, primary_key=True)
    pwd = Column(Text)
    owner_id = Column(Text, ForeignKey('user.uid'))

class Depository(Base): #
    __tablename__ = 'depository'
    did = Column(Text, primary_key=True)
    bid = Column(Text)
    store_id = Column(Text, ForeignKey('store.sid'))
    price = Column(Float)
    stock = Column(Integer)

class Order(Base):
    __tablename__ = 'order'
    oid = Column(Text, primary_key=True)
    uid = Column(Text, ForeignKey('user.uid'))
    sid = Column(Text, ForeignKey('store.sid'))
    total_price = Column(Float)
    status = Column(Integer)

DBSession = sessionmaker(bind=engine)
session = DBSession()
Base.metadata.create_all(engine)
# session.add(User(uid='u1', login_pwd='0000'))
session.commit()
session.close()
