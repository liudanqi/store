from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
from buyer.table import User
import os
import uuid
import buyer.config
import requests
from urllib.parse import urljoin
eng = create_engine("postgresql+psycopg2://postgres:123456@127.0.0.1:5433/bookstore")
class Auth(object):
    def __init__(self, url_prefix):
        self.url_prefix = url_prefix

    def register(self,name,pwd):
        DBSession = sessionmaker(bind=eng)
        session = DBSession()
        repeat = session.query(User).filter(User.uid == name).count()
        if repeat != 0:
            session.commit()
            session.close()
            return 500
        else:
            new_player = User(uid = name ,login_pwd = pwd, money=0)
            session.add(new_player)
            session.flush()
            session.commit()
            session.close()
            return 200
    def unregister(self,name,pwd):
        DBSession = sessionmaker(bind=eng)
        session = DBSession()
        exist = session.query(User).filter(User.uid == name).count()
        if exist == 0:
            session.flush()
            session.commit()
            session.close()
            return 401
        else:
            exist_pwd = session.query(User.login_pwd).filter(User.uid == name)[0][0]
            if exist_pwd != pwd:
                session.flush()
                session.commit()
                session.close()
                return 401
            else:
                info = session.query(User).filter(User.uid == name)
                info.delete()
                session.flush()
                session.commit()
                session.close()
                return 200
    def login(self,user_id,password,terminal):
        DBSession = sessionmaker(bind=eng)
        session = DBSession()
        exist = session.query(User).filter(User.uid == user_id).count()
        if exist == 0:
            session.flush()
            session.commit()
            session.close()
            return 401,"fail"
        exist_pwd = session.query(User.login_pwd).filter(User.uid == user_id)[0][0]
        if exist_pwd != password:
            session.flush()
            session.commit()
            session.close()
            return 401,"fail"
        else:
            user = session.query(User).filter(User.uid == user_id).one()
            user.token = uuid.uuid4().hex
            x = user.token
            session.flush()
            session.commit()
            session.close()
            return 200,x

    def logout(self,user_id,token):
        DBSession = sessionmaker(bind=eng)
        session = DBSession()
        exist = session.query(User).filter(User.uid == user_id).count()
        if exist == 0:
            session.flush()
            session.commit()
            session.close()
            return 401
        user_token = session.query(User.token).filter(User.uid == user_id)[0][0]
        if token != user_token:
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
        if exist == 0:
            session.flush()
            session.commit()
            session.close()
            return 401
        old_pwd = session.query(User.login_pwd).filter(User.uid == user_id)[0][0]
        if old_pwd != old_password:
            session.flush()
            session.commit()
            session.close()
            return 401
        else:
            user = session.query(User).filter(User.uid == user_id).one()
            user.login_pwd = new_password
            session.flush()
            session.commit()
            session.close()
            return 200

    def getToken(self,user_id):
        DBSession = sessionmaker(bind=eng)
        session = DBSession()
        user_token = session.query(User.token).filter(User.uid == user_id)[0][0]
        x = user_token
        session.flush()
        session.commit()
        session.close()
        return x