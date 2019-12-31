import pytest
from be.search import Search
from test.new_seller import register_new_seller
import uuid
from test import book

class TestSearch:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_add_books_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_add_books_store_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.seller = register_new_seller(self.seller_id, self.password)
        code = self.seller.create_store(self.store_id)
        assert code == 200
        book_db = book.BookDB()
        self.books = book_db.get_book_info(0, 2)
        for b in self.books:
            code = self.seller.add_book(self.store_id, 0, b)
            assert code == 200

    def test_search(self):
        key = "美丽"
        rang = "title"
        code,_x = Search.search(self,key,rang)
        assert code == 200
