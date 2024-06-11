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
        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        Session = sessionmaker(bind=engine)
        self._session = Session()

    def get_session(self):
        return self._session

    def list_bookings(self, guest_id):
        session = self.get_session()
        bookings = session.query(Booking).filter(Booking.guest_id == guest_id).all()
        if not bookings:
            Console.format_text("No bookings found for guest_id {guest_id}")
            return []

        Console.format_text(f"Bookings for {guest_id}:", )
        for i, booking in enumerate(bookings, start=1):
            Console.format_text(f"{i}. ID: {booking.id}, Room Number: {booking.room_number},"
                                f" Start Date: {booking.start_date}, End Date: {booking.end_date}")

        while True:
            print_choice = Console.format_text("Do you want to print a booking?", "(yes/no)").lower()
            if print_choice in ['yes', 'no']:
                break
            else:
                Console.format_text("Invalid input", "Please enter 'yes' or 'no'.")

        if print_choice == 'yes':
            Console.clear()
            # Print all bookings again before asking for the booking number
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

        while True:
            choice = input("Enter the number of the booking you want to edit: ")
            if choice.isdigit() and 1 <= int(choice) <= len(bookings):
                booking = bookings[int(choice) - 1]
                break
            else:
                print("Invalid choice. Please try again.")

        fields_to_update = [
            ('number_of_guests', 'Enter new Number of Guests (press enter to skip): ',
             self.validation_manager.input_max_guests),
            ('start_date', 'Enter new Start Date (press enter to skip): ', self.validation_manager.input_start_date),
            ('end_date', 'Enter new End Date (press enter to skip): ', self.validation_manager.input_end_date),
            ('comment', 'Enter new Comment (press enter to skip): ', lambda x: x)
        ]

        if role == 'admin':
            fields_to_update.insert(0, ('room_number', 'Enter new Room Number (press enter to skip): ', lambda x: x))

        for field, prompt, validation_func in fields_to_update:
            print(prompt)
            new_value = input()
            if new_value:  # if the user entered a value
                if validation_func:
                    new_value = validation_func(new_value)
                setattr(booking, field, new_value)

        session.commit()
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
            session.delete(booking)
            session.commit()
            print(f"Booking with ID {booking_id} has been deleted.")
        else:
            print("Deletion canceled.")

    def view_and_delete_booking(self, guest_id):
        bookings = self.list_bookings(guest_id)
        if not bookings:
            return

        booking_id = int(input("Enter the ID of the booking you want to delete: "))
        self.delete_booking(booking_id)

    def add_booking(self, hotel_name=None, city=None, max_guests=None, star_rating=None,
                    start_date=None, room_type=None, end_date=None, hotel_id=None, room_id=None):
        session = self.get_session()

        # Assuming hotel_id and room_id are obtained before this point
        # (e.g., from the search results).

        print(f"Hotel Name: {hotel_name}")
        print(f"Room Type: {room_type}")
        print(f"Start Date: {start_date.strftime('%d.%m.%Y')}")
        print(f"End Date: {end_date.strftime('%d.%m.%Y')}")

        # --- User Handling ---
        email = input("Please enter your email address: ").strip().lower()
        user = self.user_manager.check_existing_usernames(email)

        if user:
            guest = session.query(Guest).filter(Guest.email == email).first()
            print(f"Welcome back, {guest.firstname} {guest.lastname}. Please review your details:")
            # ... (Display guest details)
        else:
            print("Please provide your details:")
            firstname, lastname, email, city, zip, street = self.validation_manager.create_userinfo(email)
            guest = Guest(email=email, firstname=firstname, lastname=lastname, city=city, zip=zip, street=street)
            session.add(guest)
            session.commit()

        # --- Booking Details ---
        number_of_guests = self.validation_manager.input_max_guests()
        comment = input("Any comments: ").strip()

        # --- Price Calculation ---
        room = session.query(Room).filter(Room.id == room_id).first()
        if not room:
            print("Room information not found.")
            return

        total_days = (end_date - start_date).days
        total_price = total_days * room.price_per_night
        print(f"Total Price: {total_price} for {total_days} nights.")

        # --- Confirmation ---
        confirmation = input("Do you confirm the booking? (yes/no): ")
        if confirmation.lower() != 'yes':
            print("Booking cancelled.")
            return

        # --- Create and Store Booking ---
        new_booking = Booking(
            room_hotel_id=hotel_id,
            room_number=room_id,  # Assuming you want to store the Room ID, not the number
            guest_id=guest.id,
            number_of_guests=number_of_guests,
            start_date=start_date,
            end_date=end_date,
            comment=comment,
            total_price=total_price
        )

        session.add(new_booking)
        session.commit()
        print("Booking has been successfully added.")
