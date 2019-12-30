from sqlalchemy.orm import sessionmaker
from buyer.table import Store,User,Depository
from buyer.table import engine
import time

class Buyer():
    def __init__(self, url, user_id, password):
        self.url = url
        self.user_id = user_id
        self.password = password


    def new_order(self,user_id, store_id, books):
        order_id = user_id + time.strftime("%d/%m/%Y %sH:%M:%S")  # 利用用户名+当前时间做订单编号
        total = 0 #商品价格
        #engine = create_engine("postgresql+psycopg2://postgres:123456@127.0.0.1:5433/bookstore")
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        try:
            session.query(User).filter_by(uid=user_id).count()
        except:
            session.close()
            return 511, "买家用户ID不存在"         #non exist user id
        try:
            session.query(Store).filter_by(sid = store_id).count()
        except:
            session.close()
            return 513, "商铺ID不存在"   #non exist store id
        try:
            for item in books:
                book = session.query(Depository).filter(Store.sid == store_id, Depository.bid == item.id).one()
                if(item.count >  book.stock):
                    session.close()
                    return 504,"商品库存不足"
                else:
                    total = item.count * book.price
        except:
            session.close()
            return 503, "购买的图书不存在"

        neworder = Order(order_id,user_id,store_id,total,0)
        session.add(neworder)
        session.flush()
        session.commit()
        session.close()
        return 200, "下单成功", order_id


    def payment(self,user_id, order_id):
        #engine = create_engine("postgresql+psycopg2://postgres:123456@127.0.0.1:5433/bookstore")
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        try:
            order = session.query(Order).filter(oid == order_id).one
        except:
            session.close()
            return 502, "无效参数"
        total = order.total_price
        user = session.query(User).filter(uid == user_id)
        money = user.money
        if total > money:
            session.close()
            return 501, "账户余额不足"
        else:
            user.money = user.money - total
            session.commit()
            session.close()
            return 200, "付款成功"

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