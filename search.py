from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
from create_users import Stock
eng = create_engine("postgresql+psycopg2://postgres:123456@localhost:5432/bookstore")
class search(object):
    def __init__(self, url_prefix):
        self.url_prefix = url_prefix
    # 查询包含某个名字的字段
    def name_search(self,name):
        DBSession = sessionmaker(bind=eng)
        session = DBSession()
        books = session.query(Stock).filter(Stock.bid.like('%'+name+'%')).all()
        book = books
        session.commit()
        session.close()
        return [v.to_dict() for v in book]
    #查询某个名字且在某个价格以下的字段
    def price_search(name,upper_price):
        DBSession = sessionmaker(bind=eng)
        session = DBSession()
        books = session.query(Stock).filter(Stock.bid == name,Stock.price < upper_price).all()
        book = books
        session.commit()
        session.close()
        return [v.to_dict() for v in book]
    #查询isbn
    def isbn_search(isbn):
        DBSession = sessionmaker(bind=eng)
        session = DBSession()
        books = session.query(Stock).filter(Stock.isbn == isbn).all()
        book = books
        session.commit()
        session.close()
        return [v.to_dict() for v in book]
    #查询author
    def author_search(author):
        DBSession = sessionmaker(bind=eng)
        session = DBSession()
        books = session.query(Stock).filter(Stock.author == author).all()
        book = books
        session.commit()
        session.close()
        return [v.to_dict() for v in book]








