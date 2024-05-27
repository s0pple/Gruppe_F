# ui/UserMenu.py
from business.UserManager import UserManager
from console.console_base import Menu, MenuOption
from sqlalchemy.orm import Session


class UserMenu(Menu):
    def __init__(self, main_menu: Menu):
        super().__init__("User Menu")
        self.add_option(MenuOption("Create new user"))  # option 1
        self.add_option(MenuOption("Login"))  # option 2
        self.add_option(MenuOption("Delete user"))  # option 3
        self.add_option(MenuOption("Back"))  # option 4
        self.__main_menu = main_menu

        self.__user_manager = UserManager()

    def _navigate(self, choice: int):
        match choice:
            case 1:  # option 1 (Create new user)
                username = input("Enter Username: ")
                password = input("Enter Password: ")

                self.__user_manager.create_user(username, password)
                return self  # navigate again to this menu
            case 2:  # option 2 (Login)
                username = input("Enter Username: ")
                password = input("Enter Password: ")

                if self.__user_manager.login(username, password):
                    print("You are now logged in.")
                else:
                    print("Login failed. Please try again.")
                return self  # navigate again to this menu
            case 3:  # option 3 (Delete user)
                self.__user_manager.delete_user()
                return self  # navigate again to this menu
            case 4:  # option 4 (Back)
                return self.__main_menu  # navigate back to the main menu