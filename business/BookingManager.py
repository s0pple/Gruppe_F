import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from business.BaseManager import BaseManager
import pathlib
from datetime import datetime
from console.console_base import Console
from data_models.models import *
from business.ValidationManager import ValidationManager
from business.SearchManager import SearchManager
from business.UserManager import UserManager


class BookingManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self.validation_manager = ValidationManager()
        self.search_manager = SearchManager()
        self.user_manager = UserManager()
        # Creating a connection to the database using the DB_FILE environment variable
        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        Session = sessionmaker(bind=engine)  # Creating a session class bound to the engine
        self._session = Session()  # Initializing the session instance

    def get_session(self):
        return self._session  # Returning the current session instance for reuse

    def list_bookings(self, guest_id):
        session = self.get_session()
        bookings = session.query(Booking).filter(Booking.guest_id == guest_id).all()
        if not bookings:
            Console.format_text("No bookings found for guest_id {guest_id}")
            return []
        # Formatting and displaying the bookings for the specific guest
        Console.format_text(f"Bookings for {guest_id}:", )
        for i, booking in enumerate(bookings, start=1):
            Console.format_text(f"{i}. ID: {booking.id}, Room Number: {booking.room_number},"
                                f" Start Date: {booking.start_date}, End Date: {booking.end_date}")
        # Prompting the user if they want to print a booking
        while True:
            print_choice = Console.format_text("Do you want to print a booking?", "(yes/no)").lower()
            if print_choice in ['yes', 'no']:
                break
            else:
                Console.format_text("Invalid input", "Please enter 'yes' or 'no'.")
        # Reprint all bookings before asking for the booking number
        if print_choice == 'yes':
            Console.clear()
            Console.format_text("Bookings for guest_id", f"{guest_id}:")
            for i, booking in enumerate(bookings, start=1):
                Console.format_text(
                    f"{i}. ID: {booking.id}, Room Number: {booking.room_number}, Start Date: {booking.start_date}, End Date: {booking.end_date}")

            if len(bookings) == 1:
                booking_id = bookings[0].id
            else:
                booking_id = Console.format_text("Enter the number of the booking", "you want to print: ")
            self.print_booking(booking_id, "booking.txt")  # replace "booking.txt" with your desired filename

        return bookings

    def print_booking(self, booking_id, file_name):
        session = self.get_session()
        booking = session.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            Console.format_text(f"No booking found with ID {booking_id}")
            return

        downloads_path = os.path.join(pathlib.Path.home(), "Downloads")
        file_path = os.path.join(downloads_path, file_name)  # Get the path to the user's Downloads directory

        # Writing booking details to a file for offline access
        with open(file_path, 'w') as file:
            file.write(f"Booking ID: {booking.id}\n")
            file.write(f"Room Hotel ID: {booking.room_hotel_id}\n")
            file.write(f"Room Number: {booking.room_number}\n")
            file.write(f"Guest ID: {booking.guest_id}\n")
            file.write(f"Number of Guests: {booking.number_of_guests}\n")
            file.write(f"Start Date: {booking.start_date}\n")
            file.write(f"End Date: {booking.end_date}\n")
            file.write(f"Comment: {booking.comment}\n")
        Console.clear()
        Console.format_text(f"Booking with ID {booking_id} has been saved to {file_path}")

    def get_bookings(self, start_date: datetime = None, end_date: datetime = None, hotel_name: str = None,
                     booking_id: int = None):
        # Context manager ensures the session is properly closed after use
        with self._session as session:
            query = session.query(Booking, Hotel, Guest).join(Hotel, Booking.room_hotel_id == Hotel.id).join(Guest,
                                                                                                             Booking.guest_id == Guest.id)

            if booking_id:
                query = query.filter(Booking.id == booking_id)
            if start_date and end_date:
                query = query.filter(and_(Booking.start_date >= start_date, Booking.end_date <= end_date))

            if hotel_name:
                query = query.filter(Hotel.name.ilike(f"%{hotel_name}%"))

            results = query.order_by(Hotel.name).all()
            return results

    def edit_booking(self, user_id, role):
        session = self.get_session()
        bookings = session.query(Booking).filter(Booking.guest_id == user_id).all()
        if not bookings:
            print("No bookings found.")
            return

        for i, booking in enumerate(bookings, start=1):
            print(f"{i}. {booking}")

        # Ensuring valid booking selection from user
        while True:
            choice = input("Enter the number of the booking you want to edit: ")
            if choice.isdigit() and 1 <= int(choice) <= len(bookings):
                booking = bookings[int(choice) - 1]
                break
            else:
                print("Invalid choice. Please try again.")

        # Defining the filed to update and their validation functions
        fields_to_update = [
            ('number_of_guests', 'Enter new Number of Guests (press enter to skip): ',
             self.validation_manager.input_max_guests),
            ('start_date', 'Enter new Start Date (press enter to skip): ', self.validation_manager.input_start_date),
            ('end_date', 'Enter new End Date (press enter to skip): ', self.validation_manager.input_end_date),
            ('comment', 'Enter new Comment (press enter to skip): ', lambda x: x)
        ]

        if role == 'admin':  # Admins can also update the room
            fields_to_update.insert(0, ('room_number', 'Enter new Room Number (press enter to skip): ', lambda x: x))

        for field, prompt, validation_func in fields_to_update:
            print(prompt)
            new_value = input()
            if new_value:  # if the user entered a value
                if validation_func:
                    new_value = validation_func(new_value)  # Validate the new value
                setattr(booking, field, new_value)  # Update the booking field with the new value

        session.commit()  # Commit changes to the database
        print(f"Booking with ID {booking.id} has been updated")
        print(booking)

    def delete_booking(self, booking_id):
        session = self.get_session()
        booking = session.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            print(f"No booking found with ID {booking_id}")
            return

        confirmation = input(f"Are you sure you want to delete booking with ID {booking_id}? (yes/no): ")
        if confirmation.lower() == 'yes':
            session.delete(booking)  # Delete the booking from the database
            session.commit()  # Commit the transaction to finalize deletion
            print(f"Booking with ID {booking_id} has been deleted.")
        else:
            print("Deletion canceled.")

    def view_and_delete_booking(self, guest_id):
        bookings = self.list_bookings(guest_id)
        if not bookings:
            return

        booking_id = int(input("Enter the ID of the booking you want to delete: "))
        self.delete_booking(booking_id)  # Delete the selected booking

    def add_booking(self, hotel_name, start_date, end_date, hotel_id, room_id, guest_id, number_of_guests,
                    comment=None):
        # Create a new Booking instance
        booking = Booking(room_hotel_id=hotel_id, room_number=room_id, guest_id=guest_id, start_date=start_date,
                          end_date=end_date, number_of_guests=number_of_guests, comment=comment)

        # Add the new Booking to the session
        self._session.add(booking)

        # Commit the session to save the changes to the database
        self._session.commit()

        Console.format_text(f"Booking for {hotel_name}, room number {room_id} has been added.")

        # Prompting the user if they want to print the booking
        print_choice = Console.format_text("Do you want to print the booking?", "(yes/no)").lower()
        if print_choice == 'yes':
            self.print_booking(booking.id, "booking.txt")

