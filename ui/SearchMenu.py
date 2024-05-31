from business.SearchManager import SearchManager
from console.console_base import Menu, MenuOption


class SearchMenu(Menu):

    def __init__(self, main_menu: Menu):
        super().__init__("Search Hotel")
        self.add_option(MenuOption("Search hotels with desired attributes "))  # option 1
        self.add_option(MenuOption("Back"))  # option 2

        self.__main_menu = main_menu
        self.__search_manager = SearchManager()
        self.__select_hotel_menu = None  # Will be initialized later with hotel_id

    def get_star_rating(self):
        while True:
            try:
                input_value = input(
                    "(optional) - Enter the star rating you want to search hotels for (1-5) \n or press Enter to skip... ").strip()
                if input_value == "":
                    return None
                stars = int(input_value)
                if 1 <= stars <= 5:
                    return stars
                else:
                    print("Error: Please enter a number between 1 and 5.")
            except ValueError:
                print("Error: Invalid input. Please enter a valid number.")

    def __search_by_city_guests_star_availability(self):
        city = input("(optional) - Enter the city you want to search hotels in: ")
        max_guests = input("(optional) - Enter number of guests you want to search hotels for: ")
        star_rating = self.get_star_rating()
        start_date = input("(optional) - Enter the start date: ")
        end_date = input("(optional) - Enter the end date: ")

        all_hotels = self.__search_manager.get_hotels_by_city_guests_star_availability(city, max_guests, star_rating,
                                                                                       start_date, end_date)

        if not all_hotels:
            print("No hotels with these conditions were found")
        else:
            formatted_hotels = self.__format_hotels(all_hotels)
            choice = self.navigate_hotel(formatted_hotels)

            if choice is not None:
                choice_hotel_id = all_hotels[choice - 1].id
                print(f"You selected: {formatted_hotels[choice - 1]}")
                self.__select_hotel_menu = SelectHotelMenu(self.__main_menu, formatted_hotels, hotel_id=choice_hotel_id)
                return self.__select_hotel_menu

    def navigate_hotel(self, formatted_hotels: list):
        while True:
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
            hotel_info += "-" * 80  # Separator for better readability
            hotels_info.append(hotel_info)
        return hotels_info

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return self.__search_by_city_guests_star_availability()
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

    def __search_rooms(self, hotel_id):
        room_type = input("(optional) - Enter the room type you want to search for: ")
        max_guests = input("(optional) - Enter the maximum number of guests you want to search for: ")
        description = input("(optional) - Enter the description you want to search for: ")
        amenities = input("(optional) - Enter the amenities you want to search for: ")
        price = input("(optional) - Enter the price per night you want to search for: ")

        rooms = self.__search_manager.get_desired_rooms_by_hotel_id(hotel_id, type=room_type, max_guests=max_guests,
                                                                    description=description, amenities=amenities,
                                                                    price=price)
        if not rooms:
            print("No rooms found matching the criteria.")
        else:
            print("Available rooms:")
            for index, room in enumerate(rooms, start=1):
                room_info = (f"{index}. Room Number: {room[1]}, Type: {room[2]}, Max Guests: {room[3]}, "
                             f"Description: {room[4]}, Amenities: {room[5]}, Price per Night: {room[6]}")
                print(room_info)

            try:
                choice = int(input("Enter the number of the room you want to select: "))
                if 1 <= choice <= len(rooms):
                    selected_room = rooms[choice - 1]
                    print(
                        f"You selected: Room Number: {selected_room[1]}, Type: {selected_room[2]}, Price per Night: {selected_room[6]}")
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def _navigate(self, choice: int):
        if choice == 3:  # Search rooms in selected hotel
            if self._hotel_id is not None:
                self.__search_rooms(self._hotel_id)
            return self
        elif choice == 4:  # Back
            return self.__main_menu
        elif 1 <= choice <= len(self._options) - 2:  # Select a hotel
            self._hotel_id = self._options[choice - 1].value.id
            print(f"You selected: {self._options[choice - 1].text}")
            return self