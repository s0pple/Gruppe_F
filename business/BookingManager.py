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
        session = self.get_session()
        booking = session.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            print(f"No booking found with ID {booking_id}")
            return

        while True:
            print("Which information do you want to update?")
            print("1. Room Hotel ID")
            print("2. Room Number")
            print("3. Guest ID")
            print("4. Number of Guests")
            print("5. Start Date")
            print("6. End Date")
            print("7. Comment")
            print("8. Guest Firstname")
            print("9. Guest Lastname")
            print("0. Nothing else")

            choice = input("Enter your choice: ")

            if choice == '1':
                booking.room_hotel_id = input("Enter new Room Hotel ID: ")
            elif choice == '2':
                booking.room_number = input("Enter new Room Number: ")
            elif choice == '3':
                booking.guest_id = input("Enter new Guest ID: ")
            elif choice == '4':
                booking.number_of_guests = input("Enter new Number of Guests: ")
            elif choice == '5':
                start_date_str = input("Enter new Start Date (YYYY-MM-DD): ")
                booking.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()  # convert the string to a date object
            elif choice == '6':
                end_date_str = input("Enter new End Date (YYYY-MM-DD): ")
                booking.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()  # convert the string to a date object
            elif choice == '7':
                booking.comment = input("Enter new Comment: ")
            elif choice == '8':
                guest = session.query(Guest).filter(Guest.id == booking.guest_id).first()
                if guest:
                    guest.firstname = input("Enter new Guest Firstname: ")
            elif choice == '9':
                guest = session.query(Guest).filter(Guest.id == booking.guest_id).first()
                if guest:
                    guest.lastname = input("Enter new Guest Lastname: ")
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")

        session.commit()
        print(f"Booking with ID {booking_id} has been updated")
        print(booking)
        