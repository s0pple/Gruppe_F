from business.SearchManager import SearchManager
from console.console_base import Menu, MenuOption
from datetime import datetime


class SearchMenu(Menu):

    def __init__(self, main_menu: Menu):
        super().__init__("Search Hotel")
        self.add_option(MenuOption("Search hotels with desired attributes "))  # option 6, cleaned 1
        self.add_option(MenuOption("Back"))  # option 7 cleaned 2

        # self.add_option(MenuOption("Select Hotel"))  # Option3
        self.__main_menu = main_menu  # we need the main menu to navigate back to it
        self.__search_manager = SearchManager()  # we need the  SearchManager to navigate back to it
        # self.__select_hotel = SelectHotel(self)
        #self.__select_hotel_menu = SelectHotelMenu(self, all_hotels =None)
        self.__select_hotel_menu = SelectHotelMenu(self, all_hotels=[], names=[])


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



    def get_max_guests(self):
        while True:
            input_value = input("(optional) - Enter number of guests you want to search hotels for: ").strip()
            if input_value == "":
                return None
            try:
                max_guests = int(input_value)
                if max_guests > 0:
                    return max_guests
                else:
                    print("Error: Please enter a positive number.")
            except ValueError:
                print("Error: Invalid input. Please enter a valid number.")
    def get_star_rating(self):
        while True:
            try:
                input_value = input(
                    "(optional) - Enter the star rating you want to search hotels for (1-5): ").strip()
                if input_value == "":
                    return None
                stars = int(input_value)
                if 1 <= stars <= 5:
                    return stars
                else:
                    print("Error: Please enter a number between 1 and 5.")
            except ValueError:
                print("Error: Invalid input. Please enter a valid number.")

    def get_start_date(self):
        while True:
            start_date = input("(optional) - Enter the start date (dd.mm.yyyy): ")
            if not start_date:
                return None  # If the input is optional and user does not enter anything, return None

            try:
                # Check if the date is in the correct format
                date_obj_start = datetime.strptime(start_date, "%d.%m.%Y")

                # Check if the date is not in the past
                if date_obj_start < datetime.now():
                    print("The date cannot be in the past. Please enter a future date.")
                    continue

                # Format the date to yyyy-mm-dd
                # formatted_start_date = date_obj_start.strftime("%Y-%m-%d")
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
                # Check if the date is in the correct format
                date_obj_end = datetime.strptime(end_date, "%d.%m.%Y")

                # Check if the date is not in the past
                if date_obj_end < datetime.now():
                    print("The date cannot be in the past. Please enter a future date.")
                    continue

                # Format the date to yyyy-mm-dd
                # formatted_end_date = date_obj.strftime("%Y-%m-%d")

                if date_obj_end < date_obj_start: #if formatted_end_date < formatted_start_date:
                    print("The end date must be later than the start date. Please try again.")
                    continue
                return date_obj_end

            except ValueError:
                print("Invalid date format. Please enter the date in dd.mm.yyyy format.")

    def __search_by__city_guests_star_availability(self):
        while True:

            hotel_name= input("(optional) - Enter the name of a hotel: ")
            #hotelname= input("(optional) - Enter the name of the Hotel: ")
            city = input("(optional) - Enter the city you want to search hotels in: ")
            # max_guests = input("(optional) - Enter number of guests you want to search hotels for: ")
            max_guests= self.get_max_guests()
            # star_rating = input("(optional) - Enter the star rating you want to search hotels for: ")
            star_rating = self.get_star_rating()
            # start_date, end_date = self.get_start_and_end_dates()
            start_date = self.get_start_date() #input("(optional) - Enter the start date: ")
            if start_date is not None:
                end_date = self.get_end_date(start_date) #input("(optional) - Enter the end date: ")
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

                if choice is not None:
                    choice_hotel_id = all_hotels[choice - 1].id  # Get the hotel ID using the choice index
                    print(f"Selected Hotel ID: {choice_hotel_id}") #Debug-statement
                    print(f"You selected: {formatted_hotels[choice - 1]}")
                input("Press Enter to continue...")
                return choice_hotel_id

                #choice_hotel_id= all_hotels[choice - 1]
                #print(choice_hotel_id)



                # if selected_hotel:
                #     print(f"You selected: {selected_hotel}")
                # input("Press Enter to continue...")
                # hotel_id=choice_hotel_id
                # return hotel_id

    def navigate_hotel(self, formatted_hotels: list):
        while True:
            print("#" * 90 )
            for index, hotel in enumerate(formatted_hotels, start=1):
                print(f"{index}. {hotel}")
            try:
                choice = input("Enter the number of your choice, or 'x' to go back: ")
                if choice.lower() == 'x':
                    return None  # Return None to indicate going back
                choice = int(choice)
                if 1 <= choice <= len(formatted_hotels):
                    #print(f"Returning choice: {choice}")  # Debug-statement
                    return choice  # Return the choice index
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

    def _navigate(self,
                  choice: int):
        match choice:
            case 1:  # option 1 (Search by city, guests, star, availability)
                self.__search_by__city_guests_star_availability()
                return self.__select_hotel_menu  # navigate again to this menu
            case 2:  # option 2 (Back)
                return self.__main_menu  # navigate back to the main menu
            # case 3:
                return self.__select_hotel_menu   #Test of Starting "Select Hotel" manualy

####################start of SelectHotelMenu class###########################
class SelectHotelMenu(Menu):

    def __init__(self, main_menu: Menu, all_hotels: list, names=None, hotel_id=None):
        super().__init__("Select Hotel")

        self.__main_menu = main_menu  # we need the main menu to navigate back to it
        fruits = ["apfel", "birne", "banane", "kiwi"]
        for fruit in fruits:
            self.add_option(MenuOption(fruit))

        if names:
            for name in names:
                self.add_option(MenuOption(name))

        if all_hotels:
            for hotel in all_hotels:
                self.add_option(MenuOption(hotel))


        self.add_option(MenuOption("Back"))  # option 7 cleaned 2
        # self.__formatted_hotels = formatted_hotels
        self.__search_manager = SearchManager()  # we need the  SearchManager to navigate back to it
        # self.__select_hotel = SelectHotel(self)
        self._hotel_id = hotel_id # storing the hotel_id

        # self.__navigate_hotel(formatted_hotels)
        # for hotels in formatted_hotels:
        #     self.add_option(MenuOption(hotels))

    # def __navigate_hotel(self, formatted_hotels: list):
    #     while True:
    #         for index, hotel in enumerate(formatted_hotels, start=1):
    #             print(f"{index}.\n {hotel}")
    #         try:
    #             choice = input("Enter Selection ")
    #
    #             if choice.lower() == 'x':
    #                 return None  # Return None to indicate going back
    #             choice = int(choice)
    #             if 1 <= choice <= len(formatted_hotels):
    #                 return formatted_hotels[choice - 1]
    #             else:
    #                 print("Invalid number. Please try again.")
    #         except ValueError:
    #             print("Invalid input. Please enter a number.")

    def __search_rooms(self, hotel_id):
        # Prompt the user for the room attributes
        room_type = input("(optional) - Enter the room type you want to search for: ")
        max_guests = input("(optional) - Enter the maximum number of guests you want to search for: ")
        description = input("(optional) - Enter the description you want to search for: ")
        amenities = input("(optional) - Enter the amenities you want to search for: ")
        price = input("(optional) - Enter the price per night you want to search for: ")

        # Call the get_desired_rooms_by_hotel_id function with the user's inputs
        rooms = self.__search_manager.get_desired_rooms_by_hotel_id(hotel_id, type=room_type, max_guests=max_guests,
                                                                    description=description, amenities=amenities,
                                                                    price=price)
        for room in rooms:
            # Print the room details
            room_info = f"Room Type: {room[0].type}\n"  # Changed 'room_type' to 'type'
            room_info += f"Max Guests: {room[0].max_guests}\n"
            room_info += f"Description: {room[0].description}\n"
            room_info += f"Amenities: {room[0].amenities}\n"
            room_info += f"Price per Night: {room[0].price}\n"
            print(room_info)

    # def _navigate(self,choice: int):
    #     match choice:
    #         case 1:  # option 6 (Search by city, guests, star, availability)
    #             print("case1")
    #             return self.__main_menu
    #         case 2: # option 2 (display rooms)
    #             print("case2")
    #             self.__display_rooms(self._hotel_id)
    #             return self.__main_menu
    #         case 3:  # option 3 (Back)
    #             print("case2")
    #             return self.__main_menu  # navigate back to the main menu

    def _navigate(self, choice: int):
        match choice:
            case 1:  # option 1 (Select a hotel)
                # Call the __search_rooms method after a hotel is selected
                self.__search_rooms(self._hotel_id)
                return self  # navigate again to this menu
            case 2:  # option 2 (Back)
                return self.__main_menu  # navigate back to the main menu