import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from business.BaseManager import BaseManager
from data_models.models import Booking
import pathlib
from datetime import datetime
from data_models.models import Booking, Hotel, Guest


class BookingManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        Session = sessionmaker(bind=engine)
        self._session = Session()

    def get_session(self):
        return self._session

    def list_bookings(self, guest_id):
        session = self.get_session()
        bookings = session.query(Booking).filter(Booking.guest_id == guest_id).all()
        if not bookings:
            print(f"No bookings found for guest_id {guest_id}")
            return []

        print(f"Bookings for guest_id {guest_id}:")
        for booking in bookings:
            print(
                f"ID: {booking.id}, Room Number: {booking.room_number}, Start Date: {booking.start_date}, End Date: {booking.end_date}")
        return bookings

    def print_booking(self, booking_id, file_name):
        session = self.get_session()
        booking = session.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            print(f"No booking found with ID {booking_id}")
            return

        # Get the path to the user's Downloads directory
        downloads_path = os.path.join(pathlib.Path.home(), "Downloads")
        file_path = os.path.join(downloads_path, file_name)

        with open(file_path, 'w') as file:
            file.write(f"ID: {booking.id}\n")
            file.write(f"Room Hotel ID: {booking.room_hotel_id}\n")
            file.write(f"Room Number: {booking.room_number}\n")
            file.write(f"Guest ID: {booking.guest_id}\n")
            file.write(f"Number of Guests: {booking.number_of_guests}\n")
            file.write(f"Start Date: {booking.start_date}\n")
            file.write(f"End Date: {booking.end_date}\n")
            file.write(f"Comment: {booking.comment}\n")
        print(f"Booking with ID {booking_id} has been saved to {file_path}")

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

    def edit_booking(self, booking_id):
        from business.ValidationManager import ValidationManager
        validation_manager = ValidationManager()
        session = self.get_session()
        booking = session.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            print(f"No booking found with ID {booking_id}")
            return

        valid_choices = ['1', '2', '3', '4', '5', '6', '0']  # list of valid choices

        while True:
            print("Which information do you want to update?")
            print("1. Room Hotel ID")
            print("2. Room Number")
            print("3. Number of Guests")
            print("4. Start Date")
            print("5. End Date")
            print("6. Comment")
            print("0. Nothing else")

            choice = validation_manager.input_integer("Enter your choice: ")

            if str(choice) not in valid_choices:
                print("Invalid choice. Please enter a number from the list.")
                continue

            if choice == 1:
                booking.room_hotel_id = validation_manager.input_integer("Enter new Room Hotel ID: ")
            elif choice == 2:
                booking.room_number = validation_manager.input_integer("Enter new Room Number: ")
            elif choice == 3:
                booking.number_of_guests = validation_manager.input_integer("Enter new Number of Guests: ")
            elif choice == 4:
                booking.start_date = validation_manager.input_start_date()
            elif choice == 5:
                booking.end_date = validation_manager.input_end_date(booking.start_date)
            elif choice == 6:
                booking.comment = validation_manager.input_text("Enter new Comment: ")
            elif choice == 0:
                break

        session.commit()
        print(f"Booking with ID {booking_id} has been updated")
        print(booking)
