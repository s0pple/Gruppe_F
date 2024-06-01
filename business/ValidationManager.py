import os
import webbrowser
from sqlalchemy import select, func, text, create_engine, or_, and_
from sqlalchemy.orm import sessionmaker, aliased
from business.BaseManager import BaseManager
from data_models.models import *
from datetime import datetime
from business.UserManager import UserManager

class ValidationManager:
    def __init__(self) -> None:
        super().__init__()
        self.__user_manager = UserManager()
        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        Session = sessionmaker(bind=engine)
        self._session = Session()

    def creat_userinfo(self, username: str):
        print("Pleas enter the following user-information: ")
        firstname = input("First name: ")
        lastname = input("Last name: ")
        emailaddress = username
        print("Pleas enter the following address-information: ")
        city = input("City: ")
        zip = self.input_zip()  # input("Zip Code: ")
        street = input('Street and Number ("Examplestreet 11"): ')
        return firstname, lastname, emailaddress, city, zip, street

    def input_zip(self):
        while True:
            zip = input("Zip code: ")
            if zip == int(zip):
                return zip
            else:
                print("Zip code is not valid")
                continue
    def input_max_guests(self):
        while True:
            input_value = input("Enter number of guests: ").strip()
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
                input_value = input("Enter the star rating(1-5): ").strip()
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
            start_date = input("Enter the start date (dd.mm.yyyy): ")
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
            end_date = input("Enter the end date (dd.mm.yyyy): ")
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

                if date_obj_end < date_obj_start: #if formatted_end_date < formatted_start_date:
                    print("The end date must be later than the start date. Please try again.")
                    continue
                return date_obj_end

            except ValueError:
                print("Invalid date format. Please enter the date in dd.mm.yyyy format.")

    def create_password(self,username):
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
                    self.__user_manager.create_user(username, password)
                    print("you have been successfully registered")
                    print("please login")
                    return self
                else:
                    print("Passwords are not identical, please enter them again")
            input("Press enter to continue...")
    def is_valid_email(self):
        while True:
            emailaddress=input("Please enter E-Mail address: ").strip().lower()
            if "@" in emailaddress and "." in emailaddress:
                at_index = emailaddress.index("@")
                dot_index = emailaddress.rindex(".")
                if at_index < dot_index:
                    return self
            else:
                print("Invalid E-Mail address")
                continue
