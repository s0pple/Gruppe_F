from business.SearchManager import SearchManager
from console.console_base import Menu, MenuOption
from business.ValidationManager import ValidationManager
from datetime import datetime


class SearchMenu(Menu):

    def __init__(self, main_menu: Menu):
        super().__init__("Search Hotel")
        self.add_option(MenuOption("Search hotels with desired attributes "))  # option 1
        self.add_option(MenuOption("Back"))  # option 2

        self.__main_menu = main_menu
        self.__search_manager = SearchManager()
        self.__validation_manager = ValidationManager()
        self.__select_hotel_menu = None  # Will be initialized later with hotel_id


    def __search_by_name_city_guests_star_availability(self):
        # while True:
            print("Enter the attributes you want to search with, or skip to show all hotels ")
            hotel_name= input("Enter the name of a hotel: ")
            #hotelname= input("(optional) - Enter the name of the Hotel: ")
            city = input("Enter the city you want to search hotels in: ")
            # max_guests = input("(optional) - Enter number of guests you want to search hotels for: ")
            max_guests= self.__validation_manager.input_max_guests()
            # star_rating = input("(optional) - Enter the star rating you want to search hotels for: ")
            star_rating = self.__validation_manager.input_star_rating()
            # start_date, end_date = self.get_start_and_end_dates()
            start_date = self.__validation_manager.input_start_date() #input("(optional) - Enter the start date: ")
            if start_date is not None:
                end_date = self.__validation_manager.input_end_date(start_date) #input("(optional) - Enter the end date: ")
            else:
                end_date = None
            all_hotels = self.__search_manager.get_hotels_by_city_guests_star_availability(hotel_name, city, max_guests, star_rating,
                                                                                           start_date, end_date)

            if not all_hotels:
                print("No hotels with these conditions were found")
                input("Press Enter to continue...")

            else:
                formatted_hotels = self.__format_hotels(all_hotels)  # Format the hotels
                #selected_hotel = self.navigate_hotel(formatted_hotels)  # Pass the formatted hotels to navigate_hotel
                choice = self.navigate_hotel(formatted_hotels)
        # if not all_hotels:
        #     print("No hotels with these conditions were found")
        # else:
        #     formatted_hotels = self.__format_hotels(all_hotels)
        #     choice = self.navigate_hotel(formatted_hotels)

                if choice is not None:
                    choice_hotel_id = all_hotels[choice - 1].id
                    print(f"You selected: {formatted_hotels[choice - 1]}")
                    self.__select_hotel_menu = SelectHotelMenu(self.__main_menu, formatted_hotels, hotel_id=choice_hotel_id)
                return self.__select_hotel_menu

    def navigate_hotel(self, formatted_hotels: list):
        while True:
            print("#" * 90 )
            for index, hotel in enumerate(formatted_hotels, start=1):
                print(f"{index}. {hotel}")
            try:
                choice = input("Enter the number of your choice, or 'x' to go back: ")
                if choice.lower() == 'x':
                    return None
                choice = int(choice)
                if 1 <= choice <= len(formatted_hotels):
                    return choice
                else:
                    print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def __format_hotels(self, all_hotels):
        hotels_info = []
        for hotel in all_hotels:
            hotel_info = f"Hotel Name: {hotel.name}\n"
            hotel_info += f"Address: {hotel.address.street}, {hotel.address.zip} {hotel.address.city}\n"
            hotel_info += f"Stars: {hotel.stars}\n"
            hotel_info += "-" * 90  # Separator for better readability
            hotels_info.append(hotel_info)
        return hotels_info

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return self.__search_by_name_city_guests_star_availability()
            case 2:
                return self.__main_menu

    def __display_rooms(self):
        rooms = self.__search_manager.get_desired_rooms_by_hotel_id(self._hotel_id, start_date, end_date)
        for room in rooms:
            room_info = f"Room Type: {room.type}\n"
            room_info += f"Max Guests: {room.max_guests}\n"
            room_info += f"Description: {room.description}\n"
            room_info += f"Equipment: {room.equipment}\n"
            room_info += f"Price per Night: {room.price_per_night}\n"
            room_info += f"Total Price: {room.total_price}\n"
            print(room_info)

####################start of SelectHotelMenu class###########################
class SelectHotelMenu(Menu):

    def __init__(self, main_menu: Menu, formatted_hotels: list, hotel_id=None):
        super().__init__("Select Hotel")

        self.__main_menu = main_menu
        self._hotel_id = hotel_id  # Storing the hotel_id
        self.__search_manager = SearchManager()

        for hotel in formatted_hotels:
            self.add_option(MenuOption(hotel))  # Add formatted hotel string as option

        self.add_option(MenuOption("Search rooms in selected hotel"))  # Option 3 to search rooms
        self.add_option(MenuOption("Back"))  # Option 4 to go back

    def _navigate(self, choice: int):
        if choice == 3:
            if self._hotel_id is not None:
                self.__search_rooms(self._hotel_id)
            return self
        elif choice == 4:
            return self.__main_menu
        elif 1 <= choice <= len(self._options) - 2:
            self._hotel_id = self._options[choice - 1].value.id
            print(f"You selected: {self._options[choice - 1].text}")
            return self
        else:
            print("Invalid choice. Please try again.")
            return self

    def get_start_date(self):
        while True:
            start_date = input("Enter the start date (dd.mm.yyyy): ")
            if not start_date:
                return None  # If the input is optional and user does not enter anything, return None

            try:
                # Check if the date is in the correct format
                date_obj_start = datetime.strptime(start_date, "%d.%m.%Y")

                # Check if the date is not in the past
                if date_obj_start < datetime.now():
                    print("The date cannot be in the past. Please enter a future date.")
                    continue

                return date_obj_start

            except ValueError:
                print("Invalid date format. Please enter the date in dd.mm.yyyy format.")

    def get_end_date(self, date_obj_start=None):
        if date_obj_start is None:
            print("Start date is needed to compare with the end date.")
            return None
        while True:
            end_date = input("Enter the end date (dd.mm.yyyy): ")
            if not end_date:
                print("End date is needed. ")
                continue

            try:
                date_obj_end = datetime.strptime(end_date, "%d.%m.%Y")

                if date_obj_end < datetime.now():
                    print("The date cannot be in the past. Please enter a future date.")
                    continue

                if date_obj_end < date_obj_start:
                    print("The end date must be later than the start date. Please try again.")
                    continue
                return date_obj_end

            except ValueError:
                print("Invalid date format. Please enter the date in dd.mm.yyyy format.")

    def __search_rooms(self, hotel_id):
        room_type = input("Enter the room type you want to search for: ")
        max_guests = input("Enter the maximum number of guests you want to search for: ")
        description = input("Enter the description you want to search for: ")
        amenities = input("Enter the amenities you want to search for: ")
        price = input("Enter the price per night you want to search for: ")
        start_date = self.get_start_date()  # Call get_start_date on self
        end_date = self.get_end_date(start_date) if start_date else None  # Call get_end_date on self

        query, rooms = self.__search_manager.get_desired_rooms_by_hotel_id(
            hotel_id, type=room_type, max_guests=max_guests,
            description=description, amenities=amenities, price=price,
            start_date=start_date, end_date=end_date
        )

        if not rooms:
            print("No rooms found matching the criteria.")
        else:
            print("\nAvailable rooms:")
            room_counter = 1
            for room in rooms:
                room = room[0]
                hotel_name = self.__search_manager.get_hotel_name_by_id(room.hotel_id)
                room_info = (f"{room_counter}. \033[4m{hotel_name}\033[0m\n"
                             f"    Room Number: {room.number}\n"
                             f"    Type: {room.type}\n"
                             f"    Max Guests: {room.max_guests}\n"
                             f"    Description: {room.description}\n"
                             f"    Amenities: {room.amenities}\n"
                             f"    Price per Night: {room.price}\n")
                print(room_info)
                print("-" * 80)
                room_counter += 1

            try:
                choice = int(input("Enter the number of the room you want to select: "))
                if 1 <= choice < room_counter:
                    selected_room = None
                    room_counter = 1
                    for room in rooms:
                        room = room[0]
                        if room_counter == choice:
                            selected_room = room
                            break
                        room_counter += 1

                    if selected_room:
                        hotel_name = self.__search_manager.get_hotel_name_by_id(selected_room.hotel_id)
                        print("\nYou selected:")
                        selected_room_info = (f"Hotel Name: \033[4m[{hotel_name}]\033[0m\n"
                                              f"Room Number: {selected_room.number}\n"
                                              f"Type: {selected_room.type}\n"
                                              f"Price per Night: {selected_room.price}")
                        print(selected_room_info)
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")