from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
from create_users import User
import time

import requests
from urllib.parse import urljoin
eng = create_engine("postgresql+psycopg2://postgres:123456@localhost:5432/bookstore")
class Auth(object):
    # def __init__(self, url_prefix):
    #     self.url_prefix = urljoin(url_prefix, "user/")

    def register(self,name,pwd):
        DBSession = sessionmaker(bind=eng)
        session = DBSession()
        repeat = session.query(User).filter(User.uid == name).count()
        if repeat != 0:
            session.commit()
            session.close()
            return 500
        else:
            new_player = User(uid = name ,login_pwd = pwd)
            session.add(new_player)
            session.flush()
            session.commit()
            session.close()
            return 200
    def unregister(self,name,pwd):
        DBSession = sessionmaker(bind=eng)
        session = DBSession()
        exist = session.query(User).filter(User.uid == name).count()
        exist_pwd = session.query(User.login_pwd).filter(User.uid == name)[0][0]
        if exist == 0:
            session.flush()
            session.commit()
            session.close()
            return 401
        elif exist_pwd != pwd:
            session.flush()
            session.commit()
            session.close()
            return 401
        else:
            exist.delete()
            session.flush()
            session.commit()
            session.close()
            return 200
    def login(self,user_id,password,terminal):
        DBSession = sessionmaker(bind=eng)
        session = DBSession()
        exist = session.query(User).filter(User.uid == user_id).count()
        exist_pwd = session.query(User.login_pwd).filter(User.uid == user_id)[0][0]
        if exist == 0:
            session.flush()
            session.commit()
            session.close()
            return 401
        elif exist_pwd != password:
            session.flush()
            session.commit()
            session.close()
            return 401
        else:
            user = session.query(User).filter(User.uid == user_id).one()
            user.token = time.time()
            x = user.token
            session.flush()
            session.commit()
            session.close()
            return 200,x

    def logout(self,user_id,token):
        DBSession = sessionmaker(bind=eng)
        session = DBSession()
        user_token = session.query(User.token).filter(User.uid == user_id)[0][0]
        exist = session.query(User).filter(User.uid == user_id).count()
        if token != user_token:
            session.flush()
            session.commit()
            session.close()
            return 401
        elif exist == 0:
            session.flush()
            session.commit()
            session.close()
            return 401
        else:
            session.flush()
            session.commit()
            session.close()
            return 200

    def password(self,user_id,old_password,new_password):
        DBSession = sessionmaker(bind=eng)
        session = DBSession()
        exist = session.query(User).filter(User.uid == user_id).count()
        old_pwd = session.query(User.login_pwd).filter(User.uid == user_id)[0][0]
        if exist == 0:
            return 401
        elif old_pwd != old_password:
            return 401
        else:
            user = session.query(User).filter(User.uid == user_id)
            user.login_pwd = new_password
            return 200















