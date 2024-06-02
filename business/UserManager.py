from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from data_models.models import Login, Guest, Booking, Address


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
        self._session.commit()

    def create_user_information(self, firstname, lastname, emailaddress: str,  city, zip, street):
        guest = Guest(firstname=firstname, email=emailaddress,  lastname=lastname)
        address = Address(city=city, zip=zip, street=street)
        self._session.add(guest)
        self._session.commit()
        self._session.add(address)
        self._session.commit()
        # Commit the session to save the new user and login to the database


    def login(self, username: str, password: str):
        user = self._session.query(Login).filter_by(username=username, password=password).first()
        if user:
            role = 'admin' if user.role_id == 1 else 'user'
            return True, role
        else:
            return False, None

    def update_user(self, role: str):
        if role == 'admin':
            user_id = input("Enter the user ID you want to update: ")
            user_login = self._session.query(Login).filter_by(id=user_id).first()
            user_guest = self._session.query(Guest).filter_by(id=user_id).first()
        else:
            username = input("Enter your current username: ")
            password = input("Enter your current password: ")
            login_successful, _ = self.login(username, password)

            if not login_successful:
                print("Login failed. Please try again.")
                return

            user_login = self._session.query(Login).filter_by(username=username).first()
            user_guest = self._session.query(Guest).filter_by(email=username).first()

        if user_login and user_guest:
            valid_choices = ['1', '2', '3', '4', '0']  # list of valid choices

            while True:
                print("Which information do you want to update?")
                print("1. Username")
                print("2. Password")
                print("3. First Name")
                print("4. Last Name")
                print("0. Nothing else")

                choice = input("Enter your choice: ")

                if choice not in valid_choices:
                    print("Invalid choice. Please enter a number from the list.")
                    continue

                if choice == '1':
                    new_username = input("Enter your new username: ")
                    user_login.username = new_username
                    user_guest.email = new_username
                elif choice == '2':
                    new_password = input("Enter your new password: ")
                    user_login.password = new_password
                elif choice == '3':
                    new_firstname = input("Enter your new first name: ")
                    user_guest.firstname = new_firstname
                elif choice == '4':
                    new_lastname = input("Enter your new last name: ")
                    user_guest.lastname = new_lastname
                elif choice == '0':
                    break

            self._session.commit()
            print(f"User {user_login.username} has been updated.")
        else:
            print("User not found.")
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