# ui/UserMenu.py
from business.UserManager import UserManager
from business.ValidationManager import ValidationManager
from console.console_base import Menu, MenuOption
from sqlalchemy.orm import Session

from data_models.models import Guest
from ui.AdminMenu import AdminMenu


class UserMenu(Menu):
    def __init__(self, main_menu: Menu):
        super().__init__("User Menu")
        self.add_option(MenuOption("Register"))  # option 1
        self.add_option(MenuOption("Login"))  # option 2
        self.add_option(MenuOption("Delete user"))  # option 3
        self.add_option(MenuOption("Update user information"))  # option 4
        self.add_option(MenuOption("Back"))  # option 5
        self.__main_menu = main_menu

        self.__user_manager = UserManager()
        self.__validation_manager = ValidationManager()

    def _navigate(self, choice):
        choice = str(choice)  # convert choice to string
        while True:
            if choice.isdigit() and 1 <= int(choice) <= 5:
                choice = int(choice)
                match choice:
                    case 1:  # option 1 (Create a new account)
                        while True:
                            print("To create a new account:")
                            username = self.__validation_manager.is_valid_email()
                            username = str(username)
                            if not username:
                                continue

                            existing_username = self.__user_manager.check_existing_usernames(username)
                            if existing_username:
                                print("E-Mail already exists. Please choose a different E-Mail.")
                            else:
                                self.__validation_manager.create_password(username)

                                firstname, lastname, emailaddress, city, zip, street = self.__validation_manager.create_userinfo(username)
                                self.__user_manager.create_user_information(firstname, lastname, emailaddress, city, zip, street)
                                print("you have been successfully registered")
                                print("please login")
                        return self
                    case 2:  # option 2 (Login)
                        username = input("Enter E-Mail address: ")
                        password = input("Enter Password: ")

                        login_successful, role = self.__user_manager.login(username, password)
                        if login_successful:
                            print("You are now logged in.")
                            if role == 'admin':
                                return AdminMenu(self.__main_menu, role)  # pass the role to AdminMenu
                            return self
                        else:
                            print("Login failed. Please try again.")

                        return self
                    case 3:
                        self.__user_manager.delete_user()
                        return self
                    case 4:  # option 4 (Update user information)
                        self.__user_manager.update_user()
                        return self
                    case 5:  # option 5 (Back)
                        return self.__main_menu
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
                choice = input("Enter your choice: ")
