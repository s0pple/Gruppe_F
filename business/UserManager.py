# include all user-related functions here
# login, register, authenticate

from data_access.data_base import Session, Engine
from data_access.models import RegisteredGuest


class UserManager:
    @staticmethod
    def register(engine: Engine, username: str, password: str):
        with Session(engine) as session:
            new_user = RegisteredGuest(username=username, password=password)
            session.add(new_user)
            session.commit()

    @staticmethod
    def login(engine: Engine, username: str, password: str):
        with Session(engine) as session:
            user = session.query(RegisteredGuest).filter_by(username=username).first()
            if user and user.password == password:
                return True
            else:
                return False

    @staticmethod
    def authenticate(engine: Engine, username: str, password: str):
        return UserManager.login(engine, username, password)
