# ui/UserMenu.py
from business.UserManager import UserManager
from business.ValidationManager import ValidationManager
from console.console_base import Menu, MenuOption
from sqlalchemy.orm import Session

from data_models.models import Guest
from ui.AdminMenu import AdminMenu
from ui.LoggedInMenu import LoggedInMenu


class UserMenu(Menu):
    def __init__(self, main_menu: Menu):
        super().__init__("User Menu")
        self.add_option(MenuOption("Register"))  # option 1
        self.add_option(MenuOption("Login"))  # option 2
        self.add_option(MenuOption("Main Menu"))  # option 3
        self.__main_menu = main_menu

        self.__user_manager = UserManager()
        self.__validation_manager = ValidationManager()

    def _navigate(self, choice):
        choice = str(choice)  # convert choice to string
        while True:
            if choice.isdigit() and 1 <= int(choice) <= 3:
                choice = int(choice)
                match choice:
                    case 1:
                        # ... existing code ...
                        return self
                    case 2:
                        username = input("Enter E-Mail address: ")
                        password = input("Enter Password: ")

                        login_successful, role, user_id = self.__user_manager.login(username,
                                                                                    password)  # get the user ID from the login method
                        if login_successful:
                            print("You are now logged in.")
                            if role == 'admin':
                                return AdminMenu(self.__main_menu, role, user_id)  # pass the user ID to AdminMenu
                            return LoggedInMenu(self.__main_menu, role, username,
                                                user_id)  # pass the user ID to LoggedInMenu
                        else:
                            print("Login failed. Please try again.")

                        return self
                    case 3:  # option 3 (Back)
                        return self.__main_menu
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
                choice = input("Enter your choice: ")

