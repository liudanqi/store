from sqlalchemy.orm import sessionmaker
from buyer.table import User,Store,Depository,Order,engine
from buyer import auth, config
from buyer import buyer

def register_new_buyer(user_id, pwd):
    a = auth.Auth(config.URL)
    code = a.register(user_id, pwd)
    assert code == 200
    b = buyer.Buyer(config.URL, user_id, pwd)
    return b