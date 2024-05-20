# include all user-related functions here
# login, register, authenticate
###
from data_access.data_base import get_db_connection


class UserManager:
    class UserManager:
        def register(self, database_path, username, password):
            session = get_db_connection(database_path)
            new_user = User(username=username, password=password)
            session.add(new_user)
            session.commit()
