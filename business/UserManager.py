# include all user-related functions here
# login, register, authenticate
###
from sqlalchemy.testing.pickleable import User

from data_access.data_base import get_db_connection


class UserManager:
    class UserManager:
        def register(self, database_path, username, password):
            session = get_db_connection(database_path)
            new_user = User(username=username, password=password)
            session.add(new_user)
            session.commit()

    def login(self, database_path, username, password):
        session = get_db_connection(database_path)
        user = session.query(User).filter_by(username=username).first()
        if user and user.password == password:
            return True
        return False
