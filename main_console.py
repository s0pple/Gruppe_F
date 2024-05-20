from business.SearchManager import *
import business.UserManager
from business.UserManager import UserManager
from data_access import data_loader as dl
from data_access.data_base import *

database_path = './data/hotel_reservation.db'


def load_db(database_path):
    # Import relevant data classes and initialize objects for hotels, registered users, admin users and other
    init_db(database_path, True, True, True)

    get_db_connection(database_path)
    # required data
    pass


def show_welcome():
    print("Welcome to hotel reservation system <customize>")
    # add more instructions or information as desired

def show_menu():
    print("Menu: ")
    print("Print 0 to search hotels in a city")
    print("Print 1 to search hotels in a city with max_guests (per room) and optional star rating")
    print("Print 2 to register a new user")
    print("Print 3 to login as a registered user or an admin")
    print("Print x to quit the hotel reservation system")


def navigate():
    choice = input("Choose an option for your desired action: ")
    match choice:
        case 'x':
            print("Goodbye, see you soon!")
            exit()
        # call functions in SearchManager
        case '0':
            city = input("Enter the city you want to search hotels in: ")
            hotels = SearchManager.search_hotels_by_city(database_path, city)
            for hotel in hotels:
                print(hotel)
        case '1':
            city = input("Enter the city you want to search hotels in: ")
            max_guests = input("Enter the max_guests you want (per room) to search hotels for: ")
            star_rating = input("(optional) - Enter the star rating you want to search hotels for: ")
            hotels = SearchManager.search_hotels_by_city_and_max_guests_with_optional_star_rating(database_path, city, max_guests, star_rating=None)
            for hotel in hotels:
                print(hotel)
        # call functions in UserManager
        case '2':
            user_manager = UserManager()
            database_path = './data/hotel_reservation.db'
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user_manager.register(database_path, username, password)

        case '3':
            print("SoonTM")
        case _:
            print("No such option, please enter a valid choice as shown in the Menu")
            choice = input("Choose an option for your desired action: ")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # later replace with load_sqlite_db()
    load_db(database_path)

    # try:
    #     dl.load_data_from_sqlite()
    # except Exception as e:
    #     print("There was a problem in loading the database, please fix the error and try again: ", e)
    # later replace with logic to show the home page GUI of your hotel
    show_welcome()

    # can be replaced by GUI control elements to create a simple menu on the home page.
    show_menu()

    # can be replaced with individual screens for different function like register, login, search etc.
    navigate()
