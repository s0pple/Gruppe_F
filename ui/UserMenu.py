# ui/UserMenu.py
import os

from business.UserManager import UserManager
from business.ValidationManager import ValidationManager
from console.console_base import Menu, MenuOption, Console
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
                    case 1:  # option 1 (Create a new account)
                        while True:
                            Console.format_text("To create a new account:")
                            username = self.__validation_manager.is_valid_email()
                            username = str(username)
                            if not username:
                                continue

                            existing_username = self.__user_manager.check_existing_usernames(username)
                            if existing_username:
                                Console.format_text("E-Mail already exists. Please choose a different E-Mail.")
                            else:
                                self.__validation_manager.create_password(username)

                                firstname, lastname, emailaddress, city, zip, street = self.__validation_manager.create_userinfo(
                                    username)
                                self.__user_manager.create_user_information(firstname, lastname, emailaddress, city,
                                                                            zip, street)
                                Console.format_text("you have been successfully registered")
                                Console.format_text("please login")
                            return self
                    case 2:
                        Console.clear()
                        username = Console.format_text("Login", "Enter E-Mail address: ")
                        password = Console.format_text("Login", "Enter Password: ")

                        login_successful, role, user_id = self.__user_manager.login(username, password)
                        if login_successful:
                            Console.clear()
                            Console.format_text("You are now logged in.")
                            if role == 'admin':
                                return AdminMenu(self.__main_menu, role, user_id)  # pass the user ID to AdminMenu
                            return LoggedInMenu(self.__main_menu, role, username,
                                                user_id)  # pass the user ID to LoggedInMenu
                        else:
                            Console.format_text("Login failed. Please try again.")

                        return self
                    case 3:  # option 3 (Back)
                        return self.__main_menu
            choice = Console.format_text("User Menu", "Enter your choice: ")
