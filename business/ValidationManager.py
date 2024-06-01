import os
from sqlalchemy import select, func, text, create_engine, or_, and_
from sqlalchemy.orm import sessionmaker, aliased
from business.BaseManager import BaseManager
from data_models.models import *
from datetime import datetime

class ValidationManager:
    def __init__(self) -> None:
        super().__init__()
        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        Session = sessionmaker(bind=engine)
        self._session = Session()


    def input_max_guests(self):
        while True:
            input_value = input("(optional) - Enter number of guests: ").strip()
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
                input_value = input(
                    "(optional) - Enter the star rating(1-5): ").strip()
                if input_value == "":
                    return None
                stars = int(input_value)
                if 1 <= stars <= 5:
                    return stars
                else:
                    print("Error: Please enter a number between 1 and 5.")
            except ValueError:
                print("Error: Invalid input. Please enter a valid number.")

    def input_start_date(self):
        while True:
            start_date = input("(optional) - Enter the start date (dd.mm.yyyy): ")
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

