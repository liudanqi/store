from sqlalchemy import Column, Text, DateTime, String, Integer, Float, ARRAY ,ForeignKey, create_engine, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:990514@localhost:5432/bookstore')

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    uid = Column(Text, primary_key=True)
    login_pwd = Column(Text)
    terminal = Column(Text)
    token = Column(Integer)
    pay_pwd = Column(Text)
    money = Column(Float)
    isseller = Column(Integer)

class Store(Base):
    __tablename__ = 'store'
    sid = Column(Text, primary_key=True)
    owner_id = Column(Text, ForeignKey('user.uid'))

class Depository(Base):
    __tablename__ = 'depository'
    did = Column(Text, primary_key=True)
    bid = Column(Text)
    store_id = Column(Text, ForeignKey('store.sid'))
    stock_level = Column(Integer)

class Stock(Base):
    __tablename__ = 'stock'
    bid = Column(Text, primary_key=True)
    title = Column(Text)
    author = Column(Text)
    publisher = Column(Text)
    original_title = Column(Text)
    translator = Column(Text)
    pub_year = Column(Text)
    pages = Column(Integer)
    price = Column(Integer)
    binding = Column(Text)
    isbn = Column(Text)
    author_intro = Column(Text)
    book_intro = Column(Text)
    content = Column(Text)
    tags = Column(ARRAY(Text))
    pics = Column(ARRAY(Text))
    # did = Column(ARRAY(Text), ForeignKey('depository.did'))





DBSession = sessionmaker(bind=engine)
session = DBSession()
Base.metadata.create_all(engine)
# session.add(User(uid='u1', login_pwd='0000'))
session.commit()
session.close()
