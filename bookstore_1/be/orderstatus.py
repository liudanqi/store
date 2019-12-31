from sqlalchemy.orm import sessionmaker
from be.table import Store,User,Depository,Order,Stock,engine
import time

class Order_Status:
    def __init__(self, url_prefix, user_id, password):
        self.url_prefix = url_prefix
        self.user_id = user_id
        self.password = password


    def order_status(self, order_id):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        if session.query(User).filter(User.uid == self.user_id).count() == 0:
            session.close()
            return 511, "买家用户ID不存在"
        if session.query(Order).filter(Order.oid == order_id).count() == 0:
            session.close()
            return 523, "订单不存在"
        order = session.query(Order).filter(Order.oid == order_id).first()
        status = order.status
        session.commit()
        session.close()
        return 200, status

    def my_order(self):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        if session.query(User).filter(User.uid == self.user_id).count() == 0:
            session.close()
            return 511, "买家用户ID不存在" 
        orders = session.query(Order).filter(Order.uid == self.user_id)
        order_list = []
        for order in orders:
            order_list.append([order.oid, order.uid, order.store_id, order.total, order.status, order.time])
        return 200, order_list

    '''
    在已知订单号的情况下用cancelorder接口，将该订单的status转为4
    '''
    def cancel_order(self, order_id):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        if session.query(User).filter(User.uid == self.user_id).count() == 0:
            session.close()
            return 511, "买家用户ID不存在" 
        if session.query(Order).filter(Order.oid == order_id).count() == 0:
            session.close()
            return 523, "订单不存在"
        order = session.query(Order).filter(Order.oid == order_id).first()
        if order.status != 0:
            return 524, "错误操作"
        order.status = 4 #cancel
        session.commit()
        session.close()
        return 200

    def auto_cancel_order(self):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        if session.query(User).filter(User.uid == self.user_id).count() == 0:
            session.close()
            return 511, "买家用户ID不存在"
        duration = 1800
        now_time = time.time()
        outtime_orders = session.query(Order).filter(Order.uid == self.user_id,now_time-Order.time > duration, Order.status == 0)
        for o_order in outtime_orders:
            o_order.status = 4
            session.commit()
            session.flush()
        session.close()
        return 200





