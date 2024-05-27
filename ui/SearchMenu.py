from business.SearchManager import SearchManager
from console.console_base import Menu, MenuOption


class SearchMenu(Menu):
    def __init__(self, main_menu: Menu):
        super().__init__("Search Hotel")
        self.add_option(MenuOption("Show all hotel"))  # option 1
        self.add_option(MenuOption("Search by city"))  # option 2
        self.add_option(MenuOption("Search by stars"))  # option 3
        self.add_option(MenuOption("Search hotels by city and max guests with optional star rating"))  # option 4
        self.add_option(MenuOption("display_hotel_info"))  # option 5
        # TODO: Add further MenuOptions to search by the address.city etc. of the hotels.
        self.add_option(MenuOption("Back"))  # option 5
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
            case 6:  # option 6 (Back)
                return self.__main_menu  # navigate back to the main menu
