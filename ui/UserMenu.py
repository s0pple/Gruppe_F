# ui/UserMenu.py
from business.UserManager import UserManager
from business.ValidationManager import ValidationManager
from console.console_base import Menu, MenuOption, Console
from sqlalchemy.orm import session
from data_models.models import Guest
from ui.AdminMenu import AdminMenu
from ui.RegisteredUserMenu import RegisteredUserMenu


class UserMenu(Menu):
    def __init__(self, main_menu: Menu):
        super().__init__("User Menu")
        self.add_option(MenuOption("Register"))  # option 1
        self.add_option(MenuOption("Login"))  # option 2
        self.add_option(MenuOption("Main Menu"))  # option 3
        self.__main_menu = main_menu

        self.__user_manager = UserManager(main_menu)
        self.__validation_manager = ValidationManager()

    def _navigate(self, choice):
        choice = str(choice)  # convert choice to string
        while True:
            if choice.isdigit() and 1 <= int(choice) <= 3:
                choice = int(choice)
                match choice:
                    case 1:  # option 1 (Create a new account)
                        while True:
                            mail = Console.format_text("Account Creation",
                                                       "Please enter E-Mail address: ").strip().lower()
                            username = self.__validation_manager.is_valid_email(mail)
                            username = str(username)
                            if not username:
                                continue

                            existing_username = self.__user_manager.check_existing_usernames(username)
                            if existing_username:
                                Console.format_text("E-Mail already exists. Please choose a different E-Mail.")
                                continue
                            else:
                                self.__validation_manager.create_password(username)

                                firstname, lastname, emailaddress, city, zip, street = (
                                    self.__validation_manager.create_userinfo(username))
                                self.__user_manager.create_user_information(firstname, lastname, emailaddress, city,
                                                                            zip, street)
                                Console.format_text("you have been successfully registered")
                                Console.format_text("please login")
                            return self
                    case 2:
                        Console.clear()
                        username = Console.format_text("Login", "Enter E-Mail address: ")
                        password = Console.format_text("Login", "Enter Password: ")

                        if username != 'admin':
                            username = self.__validation_manager.is_valid_email(username)

                        login_successful, menu_instance, role = self.__user_manager.login(username, password)
                        if login_successful:
                            Console.clear()
                            Console.format_text("You are now logged in.")
                            return menu_instance  # return the appropriate menu instance
                        else:
                            Console.format_text("Login failed. Please try again.")

                        return self
                    case 3:  # option 3 (Back)
                        return self.__main_menu
            choice = Console.format_text("User Menu", "Enter your choice: ")
