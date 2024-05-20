# include all user-related functions here
# login, register, authenticate
###
from sqlalchemy.testing.pickleable import User

from data_access.data_base import Session, Engine


class UserManager:
    @staticmethod
    def register(engine: Engine, username: str, password: str):
        with Session(engine) as session:
            new_user = User(username=username, password=password)
            session.add(new_user)
            session.commit()

    @staticmethod
    def login(engine: Engine, username: str, password: str):
        with Session(engine) as session:
            user = session.query(User).filter_by(username=username).first()
            if user and user.password == password:
                return True
            else:
                return False

    @staticmethod
    def get_all_users(engine: Engine):
        with Session(engine) as session:
            users = session.query(User).all()
            return users
