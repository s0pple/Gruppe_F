from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from console.console_base import Console
from data_models.models import Login, Guest, Booking, Address
from datetime import datetime


class UserManager:
    def __init__(self, main_menu=None) -> None:
        super().__init__()
        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        session = sessionmaker(bind=engine)
        self._session = session()
        self._main_menu = main_menu

    def get_session(self):
        return self._session

    # validation to check if this username already exists
    def check_existing_usernames(self, username: str):
        existing_username = self._session.query(Login).filter(Login.username == username).first()
        return existing_username

    def create_guest_user(self):
        # Create a new guest user with default values
        guest = Guest(firstname="Guest", lastname="User", email="guest@user.com", address_id=1, type='guest')
        self._session.add(guest)
        self._session.commit()
        return guest

    def create_user(self, username: str, password: str):
        # Create a new login instance for the user
        new_login = Login(username=username, password=password, role_id=2)

        # Add the new user and login to the session & commit the session
        self._session.add(new_login)
        self._session.commit()

    # After the new user has been created, the user information is entered into the database.
    def create_user_information(self, firstname, lastname, emailaddress: str, city, zip_code, street):
        # Commit the session to save the new user and login to the database
        new_address = Address(city=city, zip=zip_code, street=street)
        self._session.add(new_address)
        self._session.flush()  # To ensure that the address is written to the DB and receives an ID

        # Now the user is saved and the address_id is set
        guest = Guest(firstname=firstname, lastname=lastname, email=emailaddress, address_id=new_address.id,
                      type='registered')
        self._session.add(guest)
        self._session.commit()

    """
    checks if there is a user with the given username and password
    if its an admin user, it returns the AdminMenu instance
    if its a registered user, it returns the RegisteredUserMenu instance
    """

    def login(self, username: str, password: str):
        user = self._session.query(Login).filter_by(username=username, password=password).first()
        if user:
            role = 'admin' if user.role_id == 1 else 'user'
            if role == 'admin':
                from ui.AdminMenu import AdminMenu  # lazy import AdminMenu
                return True, AdminMenu(self._main_menu, role, user.id), role
            else:
                from ui.RegisteredUserMenu import RegisteredUserMenu  # lazy import RegisteredUserMenu
                return True, RegisteredUserMenu(self._main_menu, role, username, user.id), role
        else:
            return False, None, None

    """
    Updates a user's details based on user input. If the user is not found, a message is displayed.
    If the role is 'admin' and no user_id is provided, it prompts for one.
    Returns the menu_instance at the end.
    """

    def update_user(self, role: str, user_id=None, menu_instance=None):
        if role == 'admin' and user_id is None:
            user_id = input(Console.format_text("Update User", "Enter the user ID you want to update: "))

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
                new_value = Console.format_text("Update User", prompt)
                if new_value:  # if the user entered a value
                    if field in ['username', 'password']:
                        setattr(user_login, field, new_value)
                        if field == 'username':
                            user_guest.email = new_value
                    else:
                        setattr(user_guest, field, new_value)

            self._session.commit()
            Console.format_text(f"User {user_login.username} has been updated.")
        else:
            Console.format_text("User not found.")

        return menu_instance

    """
    Delete a user from the system. It first prompts the user for their username and password.
    If the login is successful, it retrieves the user's login and guest information from the database.
    It then checks if the user has any future bookings. If there are future bookings, it prints a message and returns.
    If there are no future bookings, it deletes all the user's bookings, their guest information, and their login information.
    Finally, it commits the changes to the database and prints a message indicating that the user has been deleted.
    If the login is not successful or the user is not found, it prints an appropriate error message.
    """

    def delete_user(self):
        username = Console.format_text("Delete User", "Enter your username: ")
        password = Console.format_text("Delete User", "Enter your password: ")
        login_successful, _, _ = self.login(username, password)

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

                    # Check if there are any future bookings
                    future_bookings = [booking for booking in user_bookings if booking.date > datetime.now()]

                    if future_bookings:
                        Console.format_text("User has future bookings. Cannot delete user.")
                        return

                    # Delete the user's booking information
                    for booking in user_bookings:
                        self._session.delete(booking)

                    # Delete the user's guest information
                    self._session.delete(user_guest)

                # Delete the user's login information
                self._session.delete(user_login)

                self._session.commit()
                Console.format_text(f"User {username} has been deleted.")
            else:
                Console.format_text("User not found.")
        else:
            Console.format_text("Login failed. Please try again.")
        return self._main_menu
