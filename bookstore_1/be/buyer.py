from sqlalchemy.orm import sessionmaker
from be.table import Store,User,Depository,Order,Stock
from be.table import engine
import time

class Buyer():
    def __init__(self, url_prefix, user_id, password):
        self.url_prefix = url_prefix
        self.user_id = user_id
        self.password = password


    def new_order(self, store_id, books):
        order_id = self.user_id + time.strftime("%d/%m/%Y %sH:%M:%S")  # 利用用户名+当前时间做订单编号
        total = 0 #商品价格
        #engine = create_engine("postgresql+psycopg2://postgres:123456@127.0.0.1:5433/bookstore")
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        if session.query(User).filter(User.uid == self.user_id).count() == 0:
            session.close()
            return 511, "买家用户ID不存在"         #non exist user id
        if session.query(Store).filter(Store.sid == store_id).count() == 0:
            session.close()
            return 513, "商铺ID不存在"   #non exist store id:
        for item in books:
            id = item[0]
            bookcount = item[1]
            book = session.query(Depository).filter(Depository.store_id == store_id, Depository.bid == id).first()
            if book != None:
                if bookcount > book.stock_level :
                    session.close()
                    return 504,"商品库存不足"
                else:
                    bookprice = session.query(Stock).filter(Stock.bid == id).one()
                    total = total + bookcount * bookprice.price
            else:
                session.close()
                return 555, "购买的图书不存在"
        session.add(Order(oid=order_id,uid=self.user_id,store_id=store_id,total=total,status=0,time=time.time()))
        session.flush()
        session.commit()
        session.close()
        return 200, order_id


    def payment(self, order_id):
        #engine = create_engine("postgresql+psycopg2://postgres:123456@127.0.0.1:5433/bookstore")
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        order = session.query(Order).filter(Order.oid == order_id).one()
        if order == None:
            session.close()
            return 520 #未找到订单
        total = order.total
        user = session.query(User).filter(User.uid == self.user_id).one()
        money = user.money
        if total > money:
            session.commit()
            session.close()
            return 519  #not sufficient funds, order id
        if user.pay_pwd != self.password:
            session.commit()
            session.close()
            return 401 #authorization fail.
        if order.status != 0:
            session.commit()
            session.close()
            return 521 #重复付款
        user.money = user.money - total
        order.status = 1
        session.commit()
        session.close()
        return 200

    def add_funds(self, add_value):
        #engine = create_engine("postgresql+psycopg2://postgres:123456@localhost:5433/bookstore")
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        exist = session.query(User).filter_by(uid=self.user_id).count()
        if exist == 0:
            session.commit()
            session.close()
            return 511
        else:
            u = session.query(User).filter_by(uid=self.user_id).first()
            if u.login_pwd != self.password:
                session.flush()
                session.commit()
                session.close()
                return 401
            else:
                u.money = u.money + add_value
                session.commit()
                return 200