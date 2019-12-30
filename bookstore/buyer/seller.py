from sqlalchemy.orm import sessionmaker
import pymongo

from buyer.table import Store,User,Depository,engine

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db=client.bookstore

class Seller():
    def __init__(self, url, user_id, pwd):
        self.url = url
        self.user_id = user_id
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
            session.add(Store(sid=sid, owner_id=self.user_id))
            session.commit()
            session.close()
            return 200


    # 添加图书
    def add_book(self, sid, stock_level, info):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        e_uid = session.query(Store).filter(Store.owner_id == self.user_id)
        e_sid = session.query(Store).filter(Store.sid == sid)
        e_bid = db.stock.find({'id': info.id, 'owner': self.user_id})
        if e_uid.count() == 0:
            session.commit()
            session.close()
            return 503   # 卖家用户ID不存在
        if e_sid.count() == 0:
            session.commit()
            session.close()
            return 502   # 商铺ID不存在
        if e_bid.count()!= 0:
            session.commit()
            session.close()
            return 504   # 图书ID已存在

        db.stock.insert(info)
        db.stock.update({'id': info.id}, {'$push': {'owner': self.user_id}})
        session.add(Depository(store_id=sid, stock_level=stock_level))

        session.commit()
        session.close()
        return 200


    # 添加库存
    def add_stock_level(self,sid,bid,add_stock_level):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        e_sid = session.query(Store).filter(Store.sid == sid)
        e_bid = db.stock.find({'id': bid, 'owner': self.user_id})
        if e_sid.count() == 0:
            session.commit()
            session.close()
            return 502   # 商铺ID不存在
        if e_bid.count()== 0:
            session.commit()
            session.close()
            return 504   # 图书ID不存在

        session.query(Depository).filter(Depository.store_id == sid, Depository.bid == bid).update({'stock_level': add_stock_level})

        session.commit()
        session.close()
        return 200


    # def register_new_seller(self, name, pwd):
    #     DBSession = sessionmaker(bind=engine)
    #     session = DBSession()
    #     repeat = session.query(User).filter(User.uid == name).count()
    #     if repeat == 0:
    #         session.commit()
    #         session.close()
    #         return 500 #用户不存在
    #     re = session.query(User).filter(User.uid == name, User.isseller == 0).count()
    #     if re != 0:
    #         session.query(User).filter(User.uid == name, User.isseller == 0).update({'isseller': 1, 'seller_pwd': pwd})
    #         session.add()
    #         session.flush()
    #         session.commit()
    #         session.close()
    #         return 200