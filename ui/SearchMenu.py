from business.BookingManager import BookingManager
from business.SearchManager import SearchManager
from console.console_base import Menu, MenuOption, Console
from business.UserManager import UserManager
from business.ValidationManager import ValidationManager
from datetime import datetime
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

    def __search_by_name_city_guests_star_availability(self):
        while True:
            # print("Enter the attributes you want to search with, or skip to show all hotels ")
            Console.format_text("Enter the attributes you want to search with, or skip to show all hotels", "press Enter to continue...")
            #Incorrect user entries are included based on the SQL statements
            hotel_name = input("Name of hotel          :")
            city = input("City                   :")

            #input in the validation manager so that it can be easily accessed,
            max_guests = self.__validation_manager.input_max_guests()
            star_rating = self.__validation_manager.input_star_rating()
            start_date = self.__validation_manager.input_start_date()
            if start_date is not None:
                end_date = self.__validation_manager.input_end_date(
                    start_date)  # input("(optional) - Enter the end date: ")
            else:
                end_date = None

            # Perform the hotel search and selection based on the provided criteria
            choice_hotel_id = self.__search_manager.get_hotels_by_city_guests_star_availability(hotel_name, city,
                                                                                                max_guests, star_rating,
                                                                                                start_date, end_date)
            if not choice_hotel_id:
                print("No hotels with these conditions were found")
                input("Press Enter to continue...")
                continue
            else:
                self.__select_hotel_menu = SelectHotelMenu(self.__main_menu, hotel_id=choice_hotel_id)
                return self.__select_hotel_menu

    def _navigate(self, choice: int):
        match choice:
            case 1:
                # Create a guest user when the user selects the "Search Hotels" option
                self.__user_manager.create_guest_user()
                return self.__search_by_name_city_guests_star_availability()
            case 2:
                Console.clear()
                return self.__main_menu  # Navigate back to the main menu


class SelectHotelMenu(Menu):

    def __init__(self, main_menu: Menu, hotel_id=None):
        super().__init__("Search Rooms")

        self.__main_menu = main_menu
        self._hotel_id = hotel_id  # Storing the hotel_id
        self.__search_manager = SearchManager()
        self.__validation_manager = ValidationManager()

        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        Session = sessionmaker(bind=engine)
        self._session = Session()

        self.add_option(MenuOption("Search rooms in selected hotel"))  # Option 1 to search rooms
        self.add_option(MenuOption("Display all available rooms"))  # Option 2 to display all available rooms
        self.add_option(MenuOption("Back"))  # Option 3 to go back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                if self._hotel_id is not None:
                    self.__search_manager.search_rooms(self._hotel_id)
                return self
            case 2:
                if self._hotel_id is not None:
                    self.__search_manager.display_all_rooms(self._hotel_id)
                return self
            case 3:
                return self.__main_menu  # Navigate back to the main menu
            case _:
                print("Invalid choice. Please enter a number between 1 and 3.")
                return self

    # def __display_all_rooms(self, hotel_id):
    #     query, rooms = self.__search_manager.get_desired_rooms_by_hotel_id(hotel_id)
    #     if not rooms:
    #         print("No rooms found.")
    #     else:
    #         print("\nAvailable rooms:")
    #         for index, room in enumerate(rooms, start=1):
    #             room = room[0]
    #             hotel_name = self.__search_manager.get_hotel_name_by_id(room.hotel_id)  # Retrieve the hotel name
    #             room_info = (f"{index}. \033[4m[{hotel_name}]\033[0m\n"
    #                          f"    Room Number: {room.number}\n"
    #                          f"    Type: {room.type}\n"
    #                          f"    Price per Night: {room.price}\n")
    #             print(room_info)
    #             print("-" * 80)
    #
    #         try:
    #             choice = int(input("Enter the number you want to select: "))
    #             if 1 <= choice <= len(rooms):
    #                 selected_room = rooms[choice - 1][0]
    #                 print(f"You selected: room number: {selected_room.number}")
    #             else:
    #                 print("Invalid selection. Please try again.")
    #         except ValueError:
    #             print("Invalid input. Please enter a valid number.")
    #         return self
    #
    # def __search_rooms(self, hotel_id):
    #     print("Select the room type you want to search for:")
    #     print("1. Single Room")
    #     print("2. Double Room")
    #     print("3. Family Room")
    #     print("4. Suite")
    #     room_type_choice = input("Enter your choice (1-4 / Enter): ")
    #
    #     room_type_dict = {
    #         "1": "single room",
    #         "2": "double room",
    #         "3": "family room",
    #         "4": "suite",
    #         "": "all",  # Default to 'all' if no choice is made
    #     }
    #
    #     room_type = room_type_dict.get(room_type_choice, "all")
    #     if room_type == "all":
    #         room_type = None  # Treat 'all' as no specific room type
    #
    #     max_guests = input("Enter the maximum number of guests you want to search for or press Enter for all: ")
    #     max_guests = int(max_guests) if max_guests.isdigit() and 1 <= int(max_guests) <= 4 else None
    #
    #     price = input("Enter the price per night you want to search for or press Enter for all: ")
    #     price = int(price) if price.isdigit() and int(price) > 0 else None
    #
    #     start_date = self.__validation_manager.input_start_date()  # Replace get_start_date with input_start_date
    #     end_date = self.__validation_manager.input_end_date(start_date) if start_date else None
    #
    #     # If all inputs are skipped, display all rooms
    #     if not any([room_type, max_guests, price, start_date, end_date]):
    #         return self.__display_all_rooms(hotel_id)
    #
    #     query, rooms = self.__search_manager.get_desired_rooms_by_hotel_id(
    #         hotel_id, type=room_type, max_guests=max_guests,
    #         price=price, start_date=start_date, end_date=end_date
    #     )
    #
    #     if not rooms:
    #         print("No rooms found matching the criteria.")
    #     else:
    #         print("\nAvailable rooms:")
    #         for index, room in enumerate(rooms, start=1):
    #             try:
    #                 hotel_name = self.__search_manager.get_hotel_name_by_id(room.Room.hotel_id)
    #                 room_info = (f"{index}. \033[4m{hotel_name}\033[0m\n"
    #                              f"    Room Number: {room.Room.number}\n"
    #                              f"    Type: {room.Room.type}\n"
    #                              f"    Price per Night: {room.Room.price}\n")
    #                 print(room_info)
    #                 print("-" * 80)
    #             except AttributeError as e:
    #                 print(f"Error: {e}. Room attributes: {room._mapping}")
    #
    #         try:
    #             choice = int(input("Enter the number you want to select: "))
    #             if 1 <= choice <= len(rooms):
    #                 selected_room = rooms[choice - 1].Room
    #                 Console.format_text(f"You selected: room number: {selected_room.number}")
    #
    #                 # Ask if the user has a login
    #                 has_login = input("Do you have a login? (yes/no): ")
    #                 if has_login.lower() == 'yes':
    #                     # If the user has a login, retrieve the Guest instance associated with that login
    #                     username = input("Enter your username: ")
    #                     password = input("Enter your password: ")
    #                     guest = self._session.query(Guest).join(Login).filter(Login.username == username,
    #                                                                           Login.password == password).first()
    #                 else:
    #                     # If the user doesn't have a login, ask for their details and create a new Guest instance
    #                     firstname = input("Enter your first name: ")
    #                     lastname = input("Enter your last name: ")
    #                     email = input("Enter your email: ")
    #                     street = input("Enter your street and house number: ")
    #                     zip = input("Enter your zip code: ")
    #                     city = input("Enter your city: ")
    #
    #                     address = Address(street=street, zip=zip, city=city)
    #                     self._session.add(address)
    #                     self._session.commit()
    #
    #                     guest = Guest(firstname=firstname, lastname=lastname, email=email, address_id=address.id)
    #                     self._session.add(guest)
    #                     self._session.commit()
    #
    #                 booking_manager = BookingManager()  # Assuming you have a BookingManager class
    #                 hotel_name = self.__search_manager.get_hotel_name_by_id(selected_room.hotel_id)
    #                 start_date = self.__validation_manager.input_start_date()
    #                 if start_date is not None:
    #                     end_date = self.__validation_manager.input_end_date(start_date)
    #                 else:
    #                     end_date = None
    #
    #                 # Ask the user for the number of guests
    #                 number_of_guests = input("Enter the number of guests: ")
    #                 number_of_guests = int(number_of_guests) if number_of_guests.isdigit() else None
    #
    #                 booking_manager.add_booking(hotel_name=hotel_name, start_date=start_date,
    #                                             end_date=end_date, hotel_id=selected_room.hotel_id,
    #                                             room_id=selected_room.number, guest_id=guest.id,
    #                                             number_of_guests=number_of_guests)
    #             else:
    #                 Console.format_text("Invalid selection. Please try again.")
    #         except ValueError:
    #             Console.format_text("Invalid input. Please enter a valid number.")
    #         return self
