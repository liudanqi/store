from sqlalchemy.orm import sessionmaker
from be.table import Store,User,Depository,Order,Stock,engine

class Delivery():
    def __init__(self, url_prefix, user_id, password):
        self.url_prefix = url_prefix
        self.user_id = user_id
        self.password = password	

    def confirm_delivery(self,order_id):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        if session.query(User).filter(User.uid == self.user_id).count() == 0:
            session.close()
            return 511, "买家用户ID不存在"
        if session.query(Order).filter(Order.oid == order_id).count() == 0:
            session.close()
            return 523, "订单不存在"
        order = session.query(Order).filter(Order.oid == order_id).first()
        order.status = 3# 已收货
        session.commit()
        session.close()
        return 200






