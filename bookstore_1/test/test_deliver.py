import pytest

from be import seller, buyer
from test.gen_book_data import GenBook
from test.new_buyer import register_new_buyer

import uuid



class TestDeliver:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_new_order_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_new_order_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_new_order_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        self.gen_book = GenBook(self.seller_id, self.store_id)

        yield

    def test_ok(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        _, self.order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code = seller.Seller.deliver(self, self.order_id)
        assert code == 200

    def test_error_non_exist_order_id(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        _, self.order_id = self.buyer.new_order(self.store_id, buy_book_id_list)

        code = seller.Seller.deliver(self, self.order_id+'_x')
        assert code != 200