# ui/MainMenu.py
from console.console_base import Menu, MenuOption
from ui.SearchMenu import SearchMenu, SelectHotelMenu
from ui.UserMenu import UserMenu


class MainMenu(Menu):
    def __init__(self):

        super().__init__("Main Menu")
        self.add_option(MenuOption("Search Hotel"))  # option 1
        self.add_option(MenuOption("User Menu"))  # option 2
        # we need the search menu to navigate to it
        self._search_menu = SearchMenu(self)
        self._user_menu = UserMenu(self)
        # TODO: Implement other SubMenus like SearchMenu
        # TODO: Add more MenuOptions for other User Stories to navigate to the implemented submenus
        self.add_option(MenuOption("Quit"))  # option 2

    def _navigate(self, choice: int):
        match choice:
            case 1:
                # return the menu for search, therefore display as next the search menu
                return self._search_menu
            # TODO: Add further navigation options according to the added MenuOptions in the constructor.
            case 2:
                return self._user_menu
            case 3:
                return None
