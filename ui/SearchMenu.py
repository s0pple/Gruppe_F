from business.SearchManager import SearchManager
from console.console_base import Menu, MenuOption


class SearchMenu(Menu):
    def __init__(self, main_menu: Menu, formatted_hotels: list = None):
        super().__init__("Search Hotel")
        self.add_option(MenuOption("Show all hotel"))  # option 1
        self.add_option(MenuOption("Search by city"))  # option 2
        self.add_option(MenuOption("Search by stars"))  # option 3
        self.add_option(MenuOption("Search hotels by city and max guests with optional star rating"))  # option 4
        self.add_option(MenuOption("display_hotel_info"))  # option 5
        self.add_option(MenuOption("Search hotels with desired attributs "))  # option 6
        # TODO: Add further MenuOptions to search by the address.city etc. of the hotels.
        self.add_option(MenuOption("Back"))  # option 7
        # we need the main menu to navigate back to it
        self.__main_menu = main_menu
        self.__search_manager = SearchManager()




    def __show_all(self):
        self.clear() # clear the console
        all_hotels = self.__search_manager.get_all_hotels()  # search all hotels with the search manager
        for hotel in all_hotels:
            print(hotel)
        input("Press Enter to continue...")

    def __search_by_city(self):
        self.clear() # clear the console
        city = input("City: ")
        hotels_by_name = self.__search_manager.get_hotels_by_city(city)  # search by name with the search manager
        for hotel in hotels_by_name:
            print(hotel)
        input("Press Enter to continue...")

    def __search_by_stars(self):
        self.clear() # clear the console
        stars = input("Hotel Stars: ")
        # TODO: Check if it is a number 1-5, if not output error and ask again... we have done that
        # TODO: implement the search by stars in the search manager and call the method
        # TODO: output the search result
        print("Implement this by next week")
        input("Press Enter to continue...")

    def __search_by_city_and_max_guests_with_optional_star_rating(self):
        self.clear()
        city = input("City: ")
        max_guests = input("Max Guests: ")
        stars = input("Star Rating (optional): ")
        if stars:
            stars = int(stars)
        hotels = self.__search_manager.search_hotels_by_city_and_max_guests_with_optional_star_rating(city, max_guests, stars)
        if hotels == 0:
            print("No hotels found")
        else:
            for hotel in hotels:
                print(hotel)
        input("Press Enter to continue...")

    def __display_hotel_info(self):
        self.clear()
        all_hotels = self.__search_manager.display_hotel_info()
        if not all_hotels:
            print("No hotels found")
        else:
            for hotel_info in all_hotels:
                print(hotel_info)
        input("Press Enter to continue...")

    def __search_by__city_guests_star_availability(self):
        self.clear()  # clear the console

        city = input("(optional) - Enter the city you want to search hotels in: ")
        max_guests = input("(optional) - Enter number of guests you want to search hotels for: ")
        star_rating = input("(optional) - Enter the star rating you want to search hotels for: ")
        start_date = input("(optional) - Enter the start date: ")
        end_date = input("(optional) - Enter the end date: ")
        self.clear()
        all_hotels = self.__search_manager.get_hotels_by_city_guests_star_availability(city, max_guests,
                                                                                          star_rating,
                                                                                          start_date, end_date)

        if not all_hotels:
            print("No hotels with these conditions were found")

        else:

            formatted_hotels = self.__format_hotels(all_hotels)
            selected_hotel = self.__navigate_hotel(formatted_hotels)

            if selected_hotel:
                self.clear()
                print(f"You selected: {selected_hotel}")
            input("Press Enter to continue...")

    def __navigate_hotel(self, formatted_hotels: list):
        while True:
            for index, hotel in enumerate(formatted_hotels, start=1):
                print(f"{index}.\n {hotel}")
            try:
                choice = input("Enter the number of your choice, or 'x' to go back: ")
                if choice.lower() == 'x':
                    return None  # Return None to indicate going back
                choice = int(choice)
                if 1 <= choice <= len(formatted_hotels):
                    return formatted_hotels[choice - 1]
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




    # TODO: Add more methods which implement the UI for further search options.

    def _navigate(self, choice: int): # TODO: Add further navigation options according to the added MenuOptions in the constructor.
        match choice:
            case 1:  # option 1 (Show all hotel)
                self.__show_all()
                return self  # navigate again to this menu
            case 2:  # option 2 (Search by name)
                self.__search_by_city()
                return self  # navigate again to this menu
            case 3:  # option 3 (Search by starts)
                self.__search_by_stars()
                return self  # navigate again to this menu
            case 4: # option 4 (Search hotels by city and max guests with optional star rating)
                self.__search_by_city_and_max_guests_with_optional_star_rating()
                return self # navigate again to this menu
            case 5: # option 5 (display_hotel_info)
                self.__display_hotel_info()
                return self # navigate again to this menu
            case 6: # option 6 (Search by city, guests, star, availability)
                self.__search_by__city_guests_star_availability()
                return self  # navigate again to this menu
            case 7:  # option 7 (Back)
                return self.__main_menu  # navigate back to the main menu


