from console.console_base import Menu, MenuOption, Console
from business.UserManager import UserManager
from business.BookingManager import BookingManager
from business.HotelManager import HotelManager
from ui.HotelMenu import HotelMenu


class AdminMenu(Menu):
    def __init__(self, main_menu: Menu, role: str, user_id: int):
        super().__init__("Admin Menu")
        self.add_option(MenuOption("Search Bookings"))
        self.add_option(MenuOption("Edit Bookings"))
        self.add_option(MenuOption("Cancel Bookings"))
        self.add_option(MenuOption("Hotel Panel"))
        self.add_option(MenuOption("Update user"))
        self.add_option(MenuOption("Delete user"))
        self.add_option(MenuOption("Logout"))
        self.__main_menu = main_menu
        self.__user_manager = UserManager()
        self.__role = role
        self.__booking_manager = BookingManager()
        self.__hotel_manager = HotelManager
        self.__hotel_menu = HotelMenu
        self.__user_id = user_id

    def _navigate(self, choice):
        if choice == 1:  # Show Bookings
            user_id = Console.format_text("Show Bookings", "Enter a user ID: ")
            if user_id.isdigit():
                self.__booking_manager.list_bookings(int(user_id))
            else:
                Console.format_text("Invalid input", "Please enter a valid number.")
            return self
        elif choice == 2:  # Edit Booking
            user_id = Console.format_text("Edit Booking", "Enter the User_ID to see bookings: ")
            self.__booking_manager.edit_booking(user_id, self.__role)
            return self
        elif choice == 3:  # Cancel Booking
            booking_id = Console.format_text("Cancel Booking", "Enter Booking ID to Cancel a Booking: ")
            self.__booking_manager.delete_booking(booking_id)
            return self
        elif choice == 4:  # Adjust hotel information
            hotel_menu = self.__hotel_menu(self.__main_menu, self.__role)
            return hotel_menu
        elif choice == 5:
            self.__user_manager.update_user(self.__role, self.__user_id, self)
            return self
        elif choice == 6:  # Delete user
            self.__user_manager.delete_user(self.__role)
            return self
        elif choice == 7:  # Back
            return self.__main_menu
        else:
            Console.format_text("Invalid choice", "Please enter a number between 1 and 7.")
            return self


