from sqlalchemy.orm import sessionmaker
from buyer.table import Store,Depository,User,engine
from buyer import auth, config
from buyer import seller

def register_new_seller(user_id, pwd):
    # DBSession = sessionmaker(bind=engine)
    # session = DBSession()
    # repeat = session.query(User).filter(User.uid == name).count()
    # if repeat == 0:
    #     session.commit()
    #     session.close()
    #     return 500 #用户不存在
    # re = session.query(User).filter(User.uid == name, User.isseller == 0).count()
    # if re != 0:
    #     session.query(User).filter(User.uid == name, User.isseller == 0).update({'isseller': 1, 'seller_pwd': pwd})
    #     session.add()
    #     session.flush()
    #     session.commit()
    #     session.close()
    #     return 200



    a = auth.Auth(config.URL)
    code = a.register(user_id, pwd)
    assert code == 200
    s = seller.Seller(config.URL, user_id, pwd)
    return s