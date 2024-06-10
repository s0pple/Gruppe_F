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

    def create_user_information(self, firstname, lastname, emailaddress: str, city, zip, street):
        #guest = Guest(firstname=firstname, email=emailaddress,  lastname=lastname)
        #address = Address(city=city, zip=zip, street=street)
        #self._session.add(guest)
        #self._session.commit()
        #self._session.add(address)
        #self._session.commit()
        # Commit the session to save the new user and login to the database
        new_address = Address(city=city, zip=zip, street=street)
        self._session.add(new_address)
        self._session.flush()  # Sicherstellen, dass die Adresse in die DB geschrieben wird und eine ID erhält

        # Jetzt den Benutzer speichern und die address_id setzen
        guest = Guest(firstname=firstname, lastname=lastname, email=emailaddress, address_id=new_address.id,
                      type='registered')
        self._session.add(guest)
        self._session.commit()

    def login(self, username: str, password: str, main_menu):
        user = self._session.query(Login).filter_by(username=username, password=password).first()
        if user:
            role = 'admin' if user.role_id == 1 else 'user'
            if role == 'admin':
                from ui.AdminMenu import AdminMenu  # lazy import AdminMenu
                return True, AdminMenu(main_menu, role, user.id), role
            else:
                from ui.RegisteredUserMenu import RegisteredUserMenu  # lazy import RegisteredUserMenu
                return True, RegisteredUserMenu(main_menu, role, username, user.id), role
        else:
            return False, None, None

    def update_user(self, role: str, user_id=None, menu_instance=None):
        if role == 'admin' and user_id is None:
            user_id = input("Enter the user ID you want to update: ")

        user_login = self._session.query(Login).filter_by(id=user_id).first()
        user_guest = self._session.query(Guest).filter_by(id=user_id).first()

        if user_login and user_guest:
            fields_to_update = [
                ('username', 'Enter your new username (press enter to skip): '),
                ('password', 'Enter your new password (press enter to skip): '),
                ('firstname', 'Enter your new first name (press enter to skip): '),
                ('lastname', 'Enter your new last name (press enter to skip): ')
            ]

            for field, prompt in fields_to_update:
                print(prompt)
                new_value = input()
                if new_value:  # if the user entered a value
                    if field in ['username', 'password']:
                        setattr(user_login, field, new_value)
                        if field == 'username':
                            user_guest.email = new_value
                    else:
                        setattr(user_guest, field, new_value)

            self._session.commit()
            print(f"User {user_login.username} has been updated.")
        else:
            print("User not found.")

        return menu_instance

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
