from business.BookingManager import BookingManager
from business.SearchManager import SearchManager
from console.console_base import Menu, MenuOption, Console
from business.UserManager import UserManager
from business.ValidationManager import ValidationManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from data_models.models import Address, Guest, Login


class SearchMenu(Menu):

    def __init__(self, main_menu: Menu):
        super().__init__("Search Hotel")
        self.add_option(MenuOption("Search hotels with desired attributes "))  # Option to search hotels
        self.add_option(MenuOption("Back"))  # Option to go back to the main menu

        self.__main_menu = main_menu
        self.__search_manager = SearchManager()
        self.__validation_manager = ValidationManager()
        self.__user_manager = UserManager()
        self.__select_hotel_menu = None  # Will be initialized later with hotel_id

    def _navigate(self, choice: int):
        match choice:
            case 1:
                # Create a guest user when the user selects the "Search Hotels" option
                self.__user_manager.create_guest_user()
                while True:
                    # print("Enter the attributes you want to search with, or skip to show all hotels ")
                    Console.format_text("Enter the attributes you want to search with, or skip to show all hotels",
                                        "press Enter to continue...")
                    # Incorrect user entries are included based on the SQL statements
                    hotel_name = input("Name of hotel          :")
                    city = input("City                   :")

                    # input in the validation manager so that it can be easily accessed,
                    max_guests = self.__validation_manager.input_max_guests()
                    star_rating = self.__validation_manager.input_star_rating()
                    start_date = self.__validation_manager.input_start_date()
                    if start_date is not None:
                        end_date = self.__validation_manager.input_end_date(
                            start_date)
                    else:
                        end_date = None

                    # Perform the hotel search and selection based on the provided criteria
                    choice_hotel_id = self.__search_manager.get_hotels_by_city_guests_star_availability(hotel_name,
                                                                                                        city,
                                                                                                        max_guests,
                                                                                                        star_rating,
                                                                                                        start_date,
                                                                                                        end_date)
                    if not choice_hotel_id:
                        continue
                    else:
                        self.__select_hotel_menu = RoomSearchAndBookingMenu(self.__main_menu, hotel_id=choice_hotel_id)
                        return self.__select_hotel_menu
            case 2:
                Console.clear()
                return self.__main_menu  # Navigate back to the main menu

class RoomSearchAndBookingMenu(Menu):
    def __init__(self, main_menu: Menu, hotel_id=None):
        super().__init__("Search Rooms")

        self.__main_menu = main_menu  # Reference to the main menu to enable navigation back to it
        self._hotel_id = hotel_id  # Storing the hotel_id to identify which hotel's rooms to search
        self.__search_manager = SearchManager()  # Initializing SearchManager for room search functionality
        self.__validation_manager = ValidationManager()  # Initializing ValidationManager for input validation

        # Setting up the database connection
        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        Session = sessionmaker(bind=engine)
        self._session = Session()

        # Adding menu options for user interaction
        self.add_option(MenuOption("Search rooms in selected hotel"))  # Option to search rooms based on criteria
        self.add_option(MenuOption("Display all available rooms"))  # Option to display all rooms without criteria
        self.add_option(MenuOption("Back"))  # Option to go back to the main menu

    def _navigate(self, choice: int):
        # Handling user selection from the menu
        match choice:
            case 1:
                if self._hotel_id is not None:
                    # If a hotel is selected, proceed with room search for that hotel
                    self.__search_manager.search_rooms(self._hotel_id)
                return self  # Return to the current menu after operation
            case 2:
                if self._hotel_id is not None:
                    # If a hotel is selected, display all available rooms for that hotel
                    self.__search_manager.display_all_rooms(self._hotel_id)
                return self  # Return to the current menu after operation
            case 3:
                # Navigate back to the main menu
                return self.__main_menu
            case _:
                # Handle invalid menu choice
                print("Invalid choice. Please enter a number between 1 and 3.")
                return self