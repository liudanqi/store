from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker
from be.table import Store,User,Depository,Order,Stock
from be.table import engine


class Search:
    def __init__(self, url_prefix, user_id, password):
        self.url_prefix = url_prefix
        self.user_id = user_id
        self.password = password

    def search(self,key,rang):
        range_list = ["all","title","tags","content"]
        r = range_list.index(rang)
        if r is None:
            return 600, "范围错误"
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        book_list = []
        if rang == "all":
            result = session.query(Stock).filter((or_(Stock.title.like("%" + key + "%"),
                                                      Stock.tags.like("%" + key + "%"),
                                                      Stock.content.like("%" + key + "%")))).all()
        result = []
        if rang == "title":
            result = session.query(Stock).filter((Stock.title.like("%" + key + "%"))).all()
        if rang == "tags":
            result = session.query(Stock).filter((Stock.tags.like("%" + key + "%"))).all()
        if rang == "content":
            result = session.query(Stock).filter((Stock.content.like("%" + key + "%"))).all()
        for i in result:
            book_searched = session.query(Depository).filter((Depository.bid == i.bid)).all()
            for book in book_searched:
                book_list.append(book)
        return 200, book_list