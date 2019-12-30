from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
import pymongo
import uuid


from be.table import Store,User,Depository,engine,Stock

class Seller():
    def __init__(self, url, user_id, pwd):
        self.url = url
        self.seller_id = user_id
        self.pwd = pwd


    # 创建商铺
    def create_store(self, sid):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        exist = session.query(Store).filter(Store.sid == sid)
        if exist.count() != 0:
            session.commit()
            session.close()
            return 501   # 商铺ID已存在
        else:
            session.add(Store(sid=sid, owner_id=self.seller_id))
            session.commit()
            session.close()
            return 200


    # 添加图书
    def add_book(self, sid, stock_level, info):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        e_uid = session.query(Store).filter(Store.owner_id == self.seller_id)
        e_sid = session.query(Store).filter(Store.sid == sid)
        bid_list = session.query(Stock).filter(Stock.bid == info.id)
        e_bid = session.query(Depository).filter(and_(Depository.bid == info.id, Depository.store_id == sid))
        if e_uid.count() == 0:
            session.flush()
            session.commit()
            session.close()
            return 503   # 卖家用户ID不存在
        if e_sid.count() == 0:
            session.flush()
            session.commit()
            session.close()
            return 502   # 商铺ID不存在
        if e_bid.count() != 0:
            session.flush()
            session.commit()
            session.close()
            return 504   # 图书ID已存在
        if bid_list.count() == 0:
            session.add(Stock(bid = info.id,
                            title = info.title,
                            author = info.author,
                            publisher = info.publisher,
                            original_title = info.original_title,
                            translator = info.translator,
                            pub_year = info.pub_year,
                            pages = info.pages,
                            price = info.price,
                            binding = info.binding,
                            isbn = info.isbn,
                            author_intro = info.author_intro,
                            book_intro = info.book_intro,
                            content = info.content,
                            tags = info.tags,
                            pics = info.pictures))
            ddid = "test_add_books_seller_id_{}".format(str(uuid.uuid1()))
            session.add(Depository(did=ddid, bid=info.id, store_id=sid, stock_level=stock_level))
            # session.query(Depository).filter(Depository.store_id == sid).update({'bid': info.id, 'stock_level': stock_level})

        else:
            ddid = "test_add_books_seller_id_{}".format(str(uuid.uuid1()))
            session.add(Depository(did=ddid, bid=info.id, store_id=sid, stock_level=stock_level))
            # session.query(Depository).filter(Depository.stock_id == sid).update({'bid': info.id, 'stock_level': stock_level})

        session.flush()
        session.commit()
        session.close()
        return 200   #添加书籍信息


    # 添加库存
    def add_stock_level(self, uid,sid,bid,add_stock_level):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        e_uid = session.query(Store).filter(Store.owner_id == uid)
        e_sid = session.query(Store).filter(Store.sid == sid)
        e_bid = session.query(Depository).filter(and_(Depository.bid == bid, Depository.store_id == sid))
        if e_uid.count() == 0:
            session.flush()
            session.commit()
            session.close()
            return 503   # 卖家用户ID不存在
        if e_sid.count() == 0:
            session.commit()
            session.close()
            return 502   # 商铺ID不存在
        if e_bid.count() == 0:
            session.commit()
            session.close()
            return 504   # 图书ID不存在

        session.query(Depository).filter(Depository.bid == bid).update({'stock_level': Depository.stock_level+add_stock_level})

        session.commit()
        session.close()
        return 200

# w = Seller('127.0.0.1:5000/', 'sss', '0000').add_book('ssss', '9', None)