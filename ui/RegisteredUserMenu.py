from console.console_base import Menu, MenuOption
from business.UserManager import UserManager
from business.BookingManager import BookingManager


class RegisteredUserMenu(Menu):
    def __init__(self, main_menu: Menu, role: str, username: str, user_id: int):
        super().__init__("User Panel")
        self.add_option(MenuOption("Show Bookings"))  # option 1
        self.add_option(MenuOption("Edit Booking"))  # option 2
        self.add_option(MenuOption("Cancel Booking"))  # option 3
        self.add_option(MenuOption("Update user"))  # option 4
        self.add_option(MenuOption("Delete user"))  # option 5
        self.add_option(MenuOption("Log out"))  # option 6

        self.__main_menu = main_menu
        self.__role = role
        self.__username = username
        self.__user_id = user_id

        self.__user_manager = UserManager()
        self.__booking_manager = BookingManager()

    def _navigate(self, choice):
        if choice == 1:  # Show Bookings
            self.__booking_manager.list_bookings(self.__user_id)
            return self
        elif choice == 2:  # Edit Booking
            self.__booking_manager.edit_booking(self.__user_id, self.__role)
            return self
        elif choice == 3:  # Cancel Booking
            self.__booking_manager.delete_booking(self.__user_id)
            return self
        elif choice == 4:  # Update user
            return self.__user_manager.update_user(self.__role, self.__user_id, self)
        elif choice == 5:  # Delete user
            self.__user_manager.delete_user()
            return self
        elif choice == 6:  # Log out
            return self.__main_menu
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")
            return self
