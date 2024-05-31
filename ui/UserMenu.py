# ui/UserMenu.py
from business.UserManager import UserManager
from console.console_base import Menu, MenuOption
from sqlalchemy.orm import Session
from ui.AdminMenu import AdminMenu
#kommentar test

class UserMenu(Menu):
    def __init__(self, main_menu: Menu):
        super().__init__("User Menu")
        self.add_option(MenuOption("Create new user"))  # option 1
        self.add_option(MenuOption("Login"))  # option 2
        self.add_option(MenuOption("Register")) # option 3
        self.add_option(MenuOption("Delete user"))  # option 4
        self.add_option(MenuOption("Back"))  # option 5
        self.__main_menu = main_menu

        self.__user_manager = UserManager()

    def _navigate(self, choice: int):
        match choice:
            case 1:  # option 1 (Create new user)
                username = input("Enter Username: ")
                while True:
                    print("Enter Passwort (capital and small letters, at least 10 characters)")
                    password = str(input("Your Password: "))
                    if len(password) >= 10:
                        if any(c.isupper() for c in password):
                            if any(c.islower() for c in password):
                                if password not in ["P123456789","Qwerty1234","Qaywsxedcr","Password12","Password123",
                                                    "Password1234","Passwort12","Passwort123", "Passwort1234"]:

                                    password_check = str(input("Enter your Password again to verify: "))
                                    if password == password_check:
                                        self.__user_manager.create_user(username, password)
                                        return self
                                    else:
                                        print("passwords are not identical, please enter them again")
                                        input("Press enter to continue...")
                                        continue
                                else:
                                    print("password too weak, please enter another one")
                                    input("Press enter to continue...")
                                    continue
                            else:
                                print("password must contain  capital and small letters, please enter it again")
                                input("Press enter to continue...")
                                continue
                        else:
                            print("password must contain  capital and small letters, please enter it again")
                            input("Press enter to continue...")
                            continue
                    else:
                        print("password must contain at least 10 characters , please enter it again")
                        input("Press enter to continue...")
                        continue

            case 2:  # option 2 (Login)
                username = input("Enter Username: ")
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