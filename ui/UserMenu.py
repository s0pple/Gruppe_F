# ui/UserMenu.py
from business.UserManager import UserManager
from business.ValidationManager import ValidationManager
from console.console_base import Menu, MenuOption
from sqlalchemy.orm import Session
from ui.AdminMenu import AdminMenu
#kommentar test

class UserMenu(Menu):
    def __init__(self, main_menu: Menu):
        super().__init__("User Menu")
        self.add_option(MenuOption("register"))  # option 1
        self.add_option(MenuOption("Login"))  # option 2
        self.add_option(MenuOption("Delete user"))  # option 3
        self.add_option(MenuOption("Back"))  # option 4
        self.__main_menu = main_menu

        self.__user_manager = UserManager()
        self.__validation_manager = ValidationManager()

    def _navigate(self, choice: int):
        match choice:
            case 1:  # option 1 (Create new user)
                while True:
                    username = input("To create a account please enter E-Mail address: ")
                    email = username
                    is_valid_email = self.__user_manager.is_valid_email(email)
                    if not is_valid_email:
                        print("Invalid E-Mail address")
                        continue

                    existing_username = self.__user_manager.check_existing_usernames(username)
                    if existing_username:
                        print("E-Mail already exists. Please choose a different E-Mail.")
                    else:
                        while True:
                            print("Enter Passwort (capital and small letters, at least 10 characters)")
                            password = input("Your Password: ")

                            if len(password) < 10:
                                print("Password must contain at least 10 characters, please enter it again")
                                continue
                            elif not any(c.isupper() for c in password):
                                print("Password must contain capital and small letters, please enter it again")
                                continue
                            elif not any(c.islower() for c in password):
                                print("Password must contain capital and small letters, please enter it again")
                                continue
                            elif password in ["P123456789", "Qwerty1234", "Qaywsxedcr", "Password12", "Password123",
                                              "Password1234", "Passwort12", "Passwort123", "Passwort1234"]:
                                print("Password too weak, please enter another one")
                                continue
                            else:
                                password_check = input("Enter your Password again to verify: ")
                                if password == password_check:
                                    self.__user_manager.create_user(username, password)
                                    print("you have been successfully registered")
                                    print("please login")
                                    return self
                                else:
                                    print("Passwords are not identical, please enter them again")
                            input("Press enter to continue...")

            case 2:  # option 2 (Login)
                username = input("Enter E-Mail address: ")
                password = input("Enter Password: ")

                login_successful, role = self.__user_manager.login(username, password)
                if login_successful:
                    print("You are now logged in.")
                    if role == 'admin':
                        return AdminMenu(self.__main_menu)
                    return self
                else:
                    print("Login failed. Please try again.")


                    return self
            case 3:
                self.__user_manager.register()
            case 4:
                self.__user_manager.delete_user()
                return self
            case 5:  # option 5 (Back)
                return self.__main_menu  #