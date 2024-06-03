import os
import webbrowser
from sqlalchemy import select, func, text, create_engine, or_, and_
from sqlalchemy.orm import sessionmaker, aliased
from business.BaseManager import BaseManager
from business.UserManager import UserManager
from data_models.models import *
from datetime import datetime


class ValidationManager:
    def __init__(self) -> None:
        super().__init__()

        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        Session = sessionmaker(bind=engine)
        self._session = Session()
        self.__user_manager = UserManager()

    def create_userinfo(self, username: str):
        print("Pleas enter the following user-information: ")
        firstname = input("First name: ")
        lastname = input("Last name: ")
        emailaddress = str(username)
        print("Pleas enter the following address-information: ")
        zip = self.input_zip()  # input("Zip Code: ")
        city = input("City: ")
        street = input('Street and Number ("Examplestreet 11"): ')
        return firstname, lastname, str(emailaddress), city, zip, street

    def input_zip(self):
        while True:
            zip_code = input("Zip code: ").strip()
            if zip_code == "":
                print("Zip code cannot be empty.")
                continue
            try:
                zip_code = int(zip_code)
                return zip_code
            except ValueError:
                print("Zip code is not valid. Please enter a valid number.")

    def input_max_guests(self):
        while True:
            input_value = input("\033[4mNumber of guests       :\033[0m    ").strip()
            if input_value == "":
                return None
            try:
                max_guests = int(input_value)
                if max_guests > 0:
                    return max_guests
                else:
                    print("Error: Please enter a positive number.")
            except ValueError:
                print("Error: Invalid input. Please enter a valid number.")

    def input_star_rating(self):
        while True:
            try:
                input_value = input("\033[4mStar rating(1-5)       :\033[0m    ").strip()
                if input_value == "":
                    return None
                stars = int(input_value)
                if 1 <= stars <= 5:
                    return stars
                if stars == 69:
                    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                    webbrowser.open(url)
                else:
                    print("Error: Please enter a number between 1 and 5.")
            except ValueError:
                print("Error: Invalid input. Please enter a valid number.")

    def input_start_date(self):
        while True:
            start_date = input("\033[4mStart date (dd.mm.yyyy):\033[0m    ")
            if not start_date:
                return None  # If the input is optional and user does not enter anything, return None

            try:
                # Check if the date is in the correct format
                date_obj_start = datetime.strptime(start_date, "%d.%m.%Y")

                # Check if the date is not in the past
                if date_obj_start < datetime.now():
                    print("The date cannot be in the past. Please enter a future date.")
                    continue

                # Format the date to yyyy-mm-dd
                # formatted_start_date = date_obj_start.strftime("%Y-%m-%d")
                return date_obj_start

            except ValueError:
                print("Invalid date format. Please enter the date in dd.mm.yyyy format.")

    def input_end_date(self, date_obj_start=None):
        if date_obj_start is None:
            print("Start date is needed to compare with the end date.")
            return None
        while True:
            end_date = input("\033[4mEnd date (dd.mm.yyyy)  :\033[0m    ")
            if not end_date:
                print("End date is needed. ")
                continue

            try:
                # Check if the date is in the correct format
                date_obj_end = datetime.strptime(end_date, "%d.%m.%Y")

                # Check if the date is not in the past
                if date_obj_end < datetime.now():
                    print("The date cannot be in the past. Please enter a future date.")
                    continue

                # Format the date to yyyy-mm-dd
                # formatted_end_date = date_obj.strftime("%Y-%m-%d")

                if date_obj_end < date_obj_start:  #if formatted_end_date < formatted_start_date:
                    print("The end date must be later than the start date. Please try again.")
                    continue
                return date_obj_end

            except ValueError:
                print("Invalid date format. Please enter the date in dd.mm.yyyy format.")

    def create_password(self, username):
        while True:
            print("Enter Passwort (capital and small letters, at least 10 characters)")
            password = input("Your Password: ")

            if len(password) < 10:
                print("Password must contain at least 10 characters, please enter it again")
                continue
            elif not any(c.isupper() for c in password):
                print("Password must contain capital and small letters, please enter it again")
                continue
            elif not any(c.islower() for c in password):
                print("Password must contain capital and small letters, please enter it again")
                continue
            elif password in ["P123456789", "Qwerty1234", "Qaywsxedcr", "Password12", "Password123",
                              "Password1234", "Passwort12", "Passwort123", "Passwort1234"]:
                print("Password too weak, please enter another one")
                continue
            else:
                password_check = input("Enter your Password again to verify: ")
                if password == password_check:
                    login = self.__user_manager.create_user(username, password)
                    return self
                else:
                    print("Passwords are not identical, please enter them again")
            input("Press enter to continue...")

    def is_valid_email(self):
        while True:
            emailaddress = str(input("Please enter E-Mail address: ")).strip().lower()
            if "@" in emailaddress and "." in emailaddress:
                at_index = emailaddress.index("@")
                dot_index = emailaddress.rindex(".")
                if at_index < dot_index:
                    return emailaddress
            else:
                print("Invalid E-Mail address")
                continue

    def input_text(self, prompt: str):
        while True:
            input_value = input(prompt)
            if isinstance(input_value, str):
                return input_value
            else:
                print("Invalid input. Please enter a text.")
                continue

    def input_integer(self, prompt: str):
        while True:
            input_value = input(prompt)
            try:
                return int(input_value)
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
                continue

    def room_max_guests(self, max_capacity):
        while True:
            input_value = input("Enter the number of guests: ").strip()
            if input_value.isdigit():
                number_of_guests = int(input_value)
                if 1 <= number_of_guests <= max_capacity:
                    return number_of_guests
                else:
                    print(f"Error: The number of guests cannot be less than 1 or more than {max_capacity}.")
            else:
                print("Error: Invalid input. Please enter a valid number.")

    def input_future_date(self, start_date=None):
        while True:
            input_date = input("Enter the date (dd.mm.yyyy): ").strip()
            try:
                date_obj = datetime.strptime(input_date, "%d.%m.%Y")
                if date_obj > datetime.now() and (start_date is None or date_obj > start_date):
                    return date_obj
                else:
                    print("Error: The date must be in the future and after the start date if provided.")
            except ValueError:
                print("Error: Invalid date format. Please enter the date in dd.mm.yyyy format.")
