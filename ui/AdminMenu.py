
from console.console_base import Menu, MenuOption
from data_models.models import Booking, Hotel
from business.UserManager import UserManager  # import UserManager


class AdminMenu(Menu):
    def __init__(self, main_menu: Menu):
        super().__init__("Admin Menu")
        self.add_option(MenuOption("Clients"))  # option 1
        self.add_option(MenuOption("Display all Bookings"))  # option 2
        self.add_option(MenuOption("Hotels"))  # option 3
        self.add_option(MenuOption("Logout"))  # option 4
        self.__main_menu = main_menu
        self.__user_manager = UserManager()  # create UserManager instance

    def _navigate(self, choice: int):
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

    def _display_all_bookings(self):
        with self.__user_manager.get_session() as session:
            results = session.query(Booking, Hotel).join(Hotel, Booking.room_hotel_id == Hotel.id).order_by(
                Hotel.name).all()

            for booking, hotel in results:
                print(
                    f"Hotel: {hotel.name}, Booking ID: {booking.id}, Guest ID: {booking.guest_id}, Start Date: {booking.start_date}, End Date: {booking.end_date}")

        while True:
            print("\n1. Return to Admin Panel")
            print("2. Logout")
            choice = input("Enter your choice: ")

            if choice == '1':
                return self
            elif choice == '2':
                return self.__main_menu
            else:
                print("Invalid choice. Please try again.")