import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from business.BaseManager import BaseManager
from data_models.models import Booking
import pathlib


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



