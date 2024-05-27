from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from data_models.models import Login


class UserManager:
    def __init__(self) -> None:
        super().__init__()
        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        Session = sessionmaker(bind=engine)
        self._session = Session()

    def get_session(self):
        return self._session

    def create_user(self, username: str, password: str):
        # Create a new login instance for the user
        new_login = Login(username=username, password=password, role_id=2)

        # Add the new user and login to the session
        self._session.add(new_login)

        # Commit the session to save the new user and login to the database
        self._session.commit()

    def login(self, username: str, password: str):
        # Query the Login table for a user with the provided username and password
        user = self._session.query(Login).filter_by(username=username, password=password).first()

        # If a user is found, print a success message and return True, else print an error message and return False
        if user:
            return True
        else:
            return False

    def update_user(self):
        # Implement the logic to update user information
        pass

    def delete_user(self):
        # Implement the logic to delete a user
        pass
