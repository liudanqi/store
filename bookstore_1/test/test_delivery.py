import pytest
import uuid
from test.new_buyer import register_new_buyer
from test.new_seller import register_new_seller
from be.delivery import Delivery
from test import book

class TestDelivery:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        '''
        生成id
        '''
        self.user_id = "test_delivery_{}".format(str(uuid.uuid1()))
        self.store_id = "test_delivery_store_id_{}".format(str(uuid.uuid1()))
        self.password = self.user_id
        '''
        注册卖家，创建商店，为了创建商店方便
        '''
        s = register_new_seller(self.user_id+"_s", self.password)
        self.seller = s
        code = s.create_store(self.store_id)
        assert code == 200
        '''
        注册买家
        '''
        b = register_new_buyer(self.user_id, self.password)
        self.buyer = b
        '''
        卖家在店里加书
        '''
        book_db = book.BookDB()
        self.books = book_db.get_book_info(0, 2)
        for bk in self.books:
            code = s.add_book(self.store_id,10,bk)
            id = bk.id
            assert code == 200
        '''
        买家下单 这里偷懒就随便用了一个书
        '''
        book_list = [[id,1]]
        code, self.order_id = b.new_order(self.store_id, book_list)
        assert code == 200
        yield

    def test_ok(self):
        code = Delivery.confirm_delivery(self,self.order_id)
        assert code == 200