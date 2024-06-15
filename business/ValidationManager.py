import os
import webbrowser
from sqlalchemy import select, func, text, create_engine, or_, and_
from sqlalchemy.orm import sessionmaker, aliased
from business.BaseManager import BaseManager
from business.UserManager import UserManager
from console.console_base import Console
from data_models.models import *
from datetime import datetime


class ValidationManager:
    def __init__(self) -> None:
        super().__init__()

        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        session = sessionmaker(bind=engine)
        self._session = session()
        self.__user_manager = UserManager()

    # Entering the user data for registration
    def create_userinfo(self, username: str):

        Console.format_text("To register Please enter the requested user-information", "Press enter to continue... ")

        firstname = Console.format_text("Register", "Enter Firstname: ")
        lastname = Console.format_text("Register", "Enter Lastname: ")
        emailaddress = str(username)
        Console.clear()
        Console.format_text("To register Please enter the requested address-information", "Press enter to continue... ")
        zip_code = self.input_zip()
        city = Console.format_text("Register", "Enter City: ").strip()
        street = Console.format_text("Register", 'Street and Number ("Examplestreet 11"): ').strip()

        Console.format_text("You have been successfully registered", "Press enter to continue... ")
        Console.clear()
        return firstname, lastname, str(emailaddress), city, zip_code, street

    # The input, formatting and validation of the zip code
    def input_zip(self):
        while True:

            zip_code = Console.format_text("Register", "Enter Zip code: ").strip()
            if zip_code == "":
                print("Zip code cannot be empty.")
                continue
            try:
                zip_code = int(zip_code)
                return zip_code
            except ValueError:
                print("Zip code is not valid. Please enter a valid number.")

    # The input, formatting and validation of the max_guest
    def input_max_guests(self):
        while True:
            input_value = input("Number of guests       :").strip()
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

    # The input, formatting and validation of the star_rating
    def input_star_rating(self):
        while True:
            try:
                input_value = input("Star rating(1-5)       :").strip()
                if input_value == "": # cancel if the input was empty
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

    # The input, formatting and validation of the start_date
    def input_start_date(self):
        while True:
            start_date = input("Start date (dd.mm.yyyy):")
            if not start_date:
                return None  # If the input is optional and user does not enter anything, return None

            try:
                # Formatting the data entry to the correct format
                date_obj_start = datetime.strptime(start_date, "%d.%m.%Y")

                # Check if the date is not in the past
                if date_obj_start < datetime.now():
                    print("The date cannot be in the past. Please enter a future date.")
                    continue

                return date_obj_start

            except ValueError:
                print("Invalid date format. Please enter the date in dd.mm.yyyy format.")

    # The input, formatting and validation of the end_date, only if the start_date has been entered
    def input_end_date(self, date_obj_start=None):
        if date_obj_start is None:
            print("Start date is needed to compare with the end date.")
            return None
        while True:
            end_date = input("End date (dd.mm.yyyy)  :")
            if not end_date:
                print("End date is needed. ")
                continue

            try:
                # Formatting the data entry to the correct format
                date_obj_end = datetime.strptime(end_date, "%d.%m.%Y")

                # Check if the date is not in the past
                if date_obj_end < datetime.now():
                    print("The date cannot be in the past. Please enter a future date.")
                    continue

                if date_obj_end < date_obj_start:
                    print("The end date must be later than the start date. Please try again.")
                    continue
                return date_obj_end

            except ValueError:
                print("Invalid date format. Please enter the date in dd.mm.yyyy format.")

    # The input and validation of the password
    def create_password(self, username):
        while True:
            password = Console.format_text("Register",
                                           "Enter Passwort (capital and small letters, at least 10 characters):").strip()

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
                password_check = Console.format_text("Register", "Enter your Password again to verify: ").strip()
                if password == password_check:
                    return self
                else:
                    print("Passwords are not identical, please enter them again")
            input("Press enter to continue...")

    # check if e-mail address can be correct
    def is_valid_email(self, mail: str):
        while True:
            if "@" in mail and "." in mail:
                at_index = mail.index("@")
                dot_index = mail.rindex(".")
                if at_index < dot_index:
                    return mail
                else:
                    print("Invalid E-Mail address")
                    mail = str(input("Please enter E-Mail address again: ")).strip().lower()

    # check if input of text is valid
    def input_text(self, prompt: str):
        while True:
            input_value = input(prompt)
            if isinstance(input_value, str):
                return input_value
            else:
                print("Invalid input. Please enter a text.")
                continue

    # check if input of number is valid
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
