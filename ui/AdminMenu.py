from console.console_base import Menu, MenuOption
from data_models.models import Booking, Hotel
from business.UserManager import UserManager  # import UserManager
from datetime import datetime
from business.BookingManager import BookingManager
from business.BookingManager import BookingManager


class AdminMenu(Menu):
    def __init__(self, main_menu: Menu, role: str):
        super().__init__("Admin Menu")
        self.add_option(MenuOption("Clients"))
        self.add_option(MenuOption("Bookings"))
        self.add_option(MenuOption("Hotels"))
        self.add_option(MenuOption("Logout"))
        self.__main_menu = main_menu
        self.__user_manager = UserManager()
        self.__role = role  # store the role for further admin functionalities like edit_booking
        self.__booking_manager = BookingManager()  # create an instance of BookingManager

    def _navigate(self):
        while True:
            choice = input("Enter your choice: ")
            if choice.isdigit() and 1 <= int(choice) <= 4:
                choice = int(choice)
                match choice:
                    case 1:
                        return self
                    case 2:
                        self._display_all_bookings()
                        return self
                    case 3:
                        return self
                    case 4:
                        return self.__main_menu
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
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
                        booking_to_modify.id)  # call the edit_booking method with the booking id
                else:
                    print("Invalid booking number. Please try again.")
            else:
                print("Invalid choice. Please try again.")
