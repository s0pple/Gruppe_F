from console.console_base import Menu, MenuOption
from business.HotelManager import HotelManager


class HotelMenu(Menu):
    def __init__(self, main_menu: Menu, role: str):
        super().__init__("HotelMenu")
        self.add_option(MenuOption("Add hotel"))  # option 1
        self.add_option(MenuOption("Edit hotel information"))  # option 2
        self.add_option(MenuOption("Add room"))  # option 3
        self.add_option(MenuOption("edit room information"))  # option 4
        self.add_option(MenuOption("Delete room"))  # option 5
        self.add_option(MenuOption("Delete hotel"))  # option 6
        self.add_option(MenuOption("Back"))  # option 7
        self.__main_menu = main_menu
        self.__hotel_manager = HotelManager(self)

    def _navigate(self, choice):
        if choice == 1:  # add hotel
            self.__hotel_manager.add_hotel()
        elif choice == 2:  # edit hotel information
            self.__hotel_manager.edit_hotel()
        elif choice == 3:  # add room
            self.__hotel_manager.add_room()
        elif choice == 4:  # edit room
            self.__hotel_manager.edit_room()
        elif choice == 5:  # delete room
            self.__hotel_manager.delete_room()
        elif choice == 6:  # delete hotel
            self.__hotel_manager.delete_hotel()
        elif choice == 7:  # Back
            return self.__main_menu
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

        return self
