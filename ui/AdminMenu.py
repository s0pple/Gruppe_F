from console.console_base import Menu, MenuOption
from data_models.models import Booking, Hotel
from business.UserManager import UserManager  # import UserManager
from datetime import datetime
from business.BookingManager import BookingManager
from business.BookingManager import BookingManager
from business.HotelManager import HotelManager
from ui.LoggedInMenu import LoggedInMenu
from ui.HotelMenu import HotelMenu


class AdminMenu(Menu):
    def __init__(self, main_menu: Menu, role: str, user_id: int):
        super().__init__("Admin Menu")
        self.add_option(MenuOption("Search Bookings"))
        self.add_option(MenuOption("Edit Bookings"))
        self.add_option(MenuOption("Cancel Bookings"))
        self.add_option(MenuOption("Adjust hotel information"))
        self.add_option(MenuOption("Update user"))
        self.add_option(MenuOption("Delete user"))
        self.add_option(MenuOption("Logout"))
        self.__main_menu = main_menu
        self.__user_manager = UserManager()
        self.__role = role
        self.__booking_manager = BookingManager()
        self.__hotel_manager = HotelManager()
        self.__hotel_menu = HotelMenu
        self.__user_id = user_id

    def _navigate(self, choice):
        if choice == 1:  # Show Bookings
            print("#" * 30)
            print("#" + "Show Bookings".center(28) + "#")
            print("#" * 30)
            user_id = input("Enter a user ID: ")
            if user_id.isdigit():
                self.__booking_manager.list_bookings(int(user_id))
            else:
                print("Invalid input. Please enter a valid number.")
            return self
        elif choice == 2:  # Edit Booking
            booking_id = input("Enter the Guest_ID to see bookings: ")
            self.__booking_manager.edit_booking(booking_id)
            return self
        elif choice == 3:  # Cancel Booking
            booking_id = input("Enter Booking ID to Cancel a Booking: ")
            self.__booking_manager.delete_booking(booking_id)
            return self
        elif choice == 4:  # Adjust hotel information
            self.__hotel_manager.edit_hotel()
            return self
        elif choice == 5:
            self.__user_manager.update_user(self.__role, self.__user_id, self)
            return self
        elif choice == 6:  # Delete user
            self.__user_manager.delete_user()
            return self
        elif choice == 7:  # Back
            return self.__main_menu
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")
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
