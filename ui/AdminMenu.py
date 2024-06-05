from console.console_base import Menu, MenuOption
from data_models.models import Booking, Hotel
from business.UserManager import UserManager  # import UserManager
from datetime import datetime
from business.BookingManager import BookingManager
from business.BookingManager import BookingManager
from business.HotelManager import HotelManager
from ui.LoggedInMenu import LoggedInMenu


class AdminMenu(Menu):
    def __init__(self, main_menu: Menu, role: str):
        super().__init__("Admin Menu")
        self.add_option(MenuOption("Clients"))
        self.add_option(MenuOption("Bookings"))
        self.add_option(MenuOption("Update user"))
        self.add_option(MenuOption("Logout"))
        self.__main_menu = main_menu
        self.__user_manager = UserManager()
        self.__role = role  # store the role for further admin functionalities like edit_booking
        self.__booking_manager = BookingManager()  # create an instance of BookingManager
        self.__hotel_manager = HotelManager() # creates an instance of HotelManager
    def _navigate(self, choice):
        if choice == 1:  # Show Bookings
            self.list_bookings(self.__user_id)
            return self
        elif choice == 2:  # Edit Booking
            # Implement the logic for editing a booking
            return self
        elif choice == 3:  # Cancel Booking
            # Implement the logic for canceling a booking
            return self
        elif choice == 4:  # Update user
            # Implement the logic for updating a user
            return self
        elif choice == 5:  # Delete user
            # Implement the logic for deleting a user
            return self
        elif choice == 6:  # Back
            return self.__main_menu
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
            return self

    def _display_all_bookings(self):
        booking_manager = BookingManager()

        booking_id = input("Enter the booking ID (leave empty to skip): ")

        start_date = None
        end_date = None
        hotel_name = None

        if not booking_id:
            hotel_name = input("Enter the hotel name (leave empty to skip): ")

            start_date_input = input("Enter the start date (YYYY-MM-DD, leave empty to skip): ")
            if start_date_input:
                start_date = datetime.strptime(start_date_input, '%Y-%m-%d')
                end_date_input = input("Enter the end date (YYYY-MM-DD): ")
                if end_date_input:
                    end_date = datetime.strptime(end_date_input, '%Y-%m-%d')

        results = booking_manager.get_bookings(start_date, end_date, hotel_name, booking_id)

        for i, (booking, hotel, guest) in enumerate(results, start=1):
            print(
                f"{i}. Hotel: {hotel.name}, Booking ID: {booking.id}, Guest ID: {booking.guest_id}, Guest First Name: {guest.firstname}, Guest Last Name: {guest.lastname}, Start Date: {booking.start_date}, End Date: {booking.end_date}")

        while True:
            print("\n1. Return to Admin Panel")
            print("2. Logout")
            if self.__role == 'admin':
                print("3. Modify a booking")
            choice = input("Enter your choice: ")

            if choice == '1':
                return self
            elif choice == '2':
                return self.__main_menu
            elif choice == '3' and self.__role == 'admin':
                # Re-display the last query results
                for i, (booking, hotel, guest) in enumerate(results, start=1):
                    print(
                        f"{i}. Hotel: {hotel.name}, Booking ID: {booking.id}, Guest ID: {booking.guest_id}, Guest First Name: {guest.firstname}, Guest Last Name: {guest.lastname}, Start Date: {booking.start_date}, End Date: {booking.end_date}")
                booking_number = int(input("Enter the number of the booking you want to modify: "))
                if 1 <= booking_number <= len(results):
                    booking_to_modify = results[booking_number - 1][0]  # get the Booking object from the results
                    booking_manager.edit_booking(
                        booking_to_modify.guest_id)  # call the edit_booking method with the guest id
                else:
                    print("Invalid booking number. Please try again.")
            else:
                print("Invalid choice. Please try again.")