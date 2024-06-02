from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from data_models.models import Login, Guest, Booking


class UserManager:
    def __init__(self) -> None:
        super().__init__()
        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        Session = sessionmaker(bind=engine)
        self._session = Session()

    def get_session(self):
        return self._session

    def check_existing_usernames(self, username: str):
        existing_username = self._session.query(Login).filter(Login.username == username).first()
        return existing_username

    def create_user(self, username: str, password: str):
        # Create a new login instance for the user
        new_login = Login(username=username, password=password, role_id=2)

        # Add the new user and login to the session
        self._session.add(new_login)

        # Commit the session to save the new user and login to the database
        self._session.commit()

    def login(self, username: str, password: str):
        user = self._session.query(Login).filter_by(username=username, password=password).first()
        if user:
            role = 'admin' if user.role_id == 1 else 'user'
            return True, role
        else:
            return False, None

    def update_user(self):
        # Implement the logic to update user information
        pass

    def delete_user(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        login_successful, _ = self.login(username, password)

        # If the login is successful, delete the user
        if login_successful:
            # Get the user's login information
            user_login = self._session.query(Login).filter_by(username=username).first()

            if user_login:
                # Get the user's guest information
                user_guest = self._session.query(Guest).filter_by(email=username).first()

                if user_guest:
                    # Get the user's booking information
                    user_bookings = self._session.query(Booking).filter_by(guest_id=user_guest.id).all()

                    # Delete the user's booking information
                    for booking in user_bookings:
                        self._session.delete(booking)

                    # Delete the user's guest information
                    self._session.delete(user_guest)

                # Delete the user's login information
                self._session.delete(user_login)

                self._session.commit()
                print(f"User {username} has been deleted.")
            else:
                print("User not found.")
        else:
            print("Login failed. Please try again.")