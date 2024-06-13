import os
from sqlalchemy import select, func, text, create_engine, or_, and_
from sqlalchemy.orm import sessionmaker, aliased
from business.BaseManager import BaseManager
from data_models.models import *
from datetime import datetime
from business.ValidationManager import ValidationManager
from console.console_base import Console

class SearchManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        # Setting up the database connection
        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        Session = sessionmaker(bind=engine)
        self._session = Session() # Initialize a session for database operations
        self.__validation_manager = ValidationManager() # Initialize validation manager for input validation

    def get_session(self):
        # Provide a method to access the current session
        return self._session

    def get_all_hotels(self) -> List[Hotel]:
        # Query to get all hotels
        query = select(Hotel)
        return self.select_all(query)

    def get_hotel_name_by_id(self, hotel_id):
        # Query to get the name of a hotel by its ID
        query = select(Hotel.name).where(Hotel.id == hotel_id)
        result = self._session.execute(query).scalar_one() # Execute the query and return a single scalar result
        return result

    def get_hotels_by_city_guests_star_availability(self, hotel_name=None, city=None, max_guests=None, star_rating=None,
                                                    start_date=None,
                                                    end_date=None) -> List[Hotel]:

        # Start building the query to get hotels with various optional filters
        query = select(Hotel).distinct().select_from(Hotel)
        if hotel_name:
            # Filter by hotel name if provided
            query = query.where(Hotel.name.ilike(f"%{hotel_name}%"))
        if city:
            # Join with Address table to filter by city
            query = query.join(Address, Hotel.address_id == Address.id).where(
                Address.city.ilike(f"%{city}%"))  # == city)

        # If max_guests is specified, add it to the WHERE clause
        if max_guests:
            query = query.where(Hotel.rooms.any(max_guests <= Room.max_guests))

        # If star_rating is specified, add it to the WHERE clause
        if star_rating:
            query = query.where(Hotel.stars == star_rating)

        # If the start_date and end_date are specified, check availability
        if start_date and end_date:
            # Alias for the Booking table to avoid name conflicts
            br = aliased(Booking)

            # Subquery to find booked room_hotel_id combinations
            booking_subquery = (
                select(br.room_hotel_id, br.room_number)
                .where(
                    or_(
                        and_(br.start_date <= start_date, br.end_date >= end_date),
                        and_(br.start_date >= start_date, br.start_date <= end_date),
                        and_(br.end_date >= start_date, br.end_date <= end_date)
                    )
                )
                .subquery()
            )

            # Main query to exclude hotels with booked rooms during the requested period
            query = query.join(Room, Hotel.id == Room.hotel_id).outerjoin(
                booking_subquery,
                and_(
                    Room.hotel_id == booking_subquery.c.room_hotel_id,
                    Room.number == booking_subquery.c.room_number
                )
            ).where(booking_subquery.c.room_hotel_id == None).group_by(Hotel.id)

        query = query.distinct(Hotel.id)

        result = self._session.execute(query)
        hotels = result.scalars().all()
        # return all_hotels
        print(hotels)

        Console.format_text("Available Hotels:")
        seen_hotel_names = set()  # Verwende ein Set, um bereits gesehene Hotelnamen zu speichern
        for i, hotel in enumerate(hotels, start=1):
            if hotel.name not in seen_hotel_names:
                Console.format_text(f"{i} \033[4m{hotel.name}\033[0m\n"
                                    f"Address: {hotel.address.street}, {hotel.address.zip} {hotel.address.city}\n"
                                    f"Stars: {hotel.stars}")
                seen_hotel_names.add(hotel.name)

        while True:
            try:
                choice = input("Enter the number of your choice, or 'x' to go back: ")
                if choice.lower() == 'x':
                    break
                choice = int(choice)
                if 1 <= choice <= len(hotels):
                    return choice  # Return the user's choice if it is valid
                else:
                    print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        if choice is not None:
            print(f"You selected: {hotels[choice - 1]}")
            choice_hotel_id = hotels[choice - 1].id
            return choice_hotel_id

    def get_all_rooms_by_hotel_id(self, hotel_id):
        query = select(Room).where(Room.hotel_id == hotel_id)
        result = self._session.execute(query)
        all_rooms = result.scalars().all()
        return all_rooms

    def get_desired_rooms_by_hotel_id(self, hotel_id=None, number=None, type=None, max_guests=None, amenities=None,
                                      price=None, description=None, start_date=None, end_date=None) -> List[Room]:
        query = select(Room)

        if hotel_id:
            query = query.where(Room.hotel_id == hotel_id)
        if number:
            query = query.where(Room.number == number)
        if type:
            query = query.where(Room.type == type)
        if max_guests:
            query = query.where(Room.max_guests == max_guests)
        if amenities:
            query = query.where(Room.amenities == amenities)
        if price:
            query = query.where(Room.price <= price)
        if description:
            query = query.where(Room.description == description)

        start_date = self.__validation_manager.input_start_date()
        if start_date is not None:
            end_date = self.__validation_manager.input_end_date(start_date)
        else:
            end_date = None

        if start_date and end_date:
            br = aliased(Booking)
            booking_subquery = (
                select(br.room_hotel_id, br.room_number)
                .where(
                    or_(
                        and_(br.start_date <= start_date, br.end_date >= end_date),
                        and_(br.start_date >= start_date, br.start_date <= end_date),
                        and_(br.end_date >= start_date, br.end_date <= end_date)
                    )
                )
                .subquery()
            )

            query = query.outerjoin(
                booking_subquery,
                and_(
                    Room.hotel_id == booking_subquery.c.room_hotel_id,
                    Room.number == booking_subquery.c.room_number
                )
            ).where(booking_subquery.c.room_hotel_id == None).group_by(Room.number)

        result = self._session.execute(query)
        all_rooms = result.fetchall()
        return self.select_all(query), all_rooms

    def display_all_rooms(self, hotel_id):
        # Display all rooms for a specific hotel
        query, rooms = self.get_desired_rooms_by_hotel_id(hotel_id)

        if not rooms:
            print("No rooms found.")
        else:
            print("\nAvailable rooms:")
            for index, room in enumerate(rooms, start=1):
                room = room[0]  # Fetch the room details from the query result
                hotel_name = self.get_hotel_name_by_id(room.hotel_id)  # Retrieve the hotel name
                room_info = (f"{index}. \033[4m{hotel_name}\033[0m\n"
                             f"    Room Number: {room.number}\n"
                             f"    Type: {room.type}\n"
                             f"    Price per Night: {room.price}\n")
                print(room_info)
                print("-" * 80)

            try:
                # Prompt the user to select a room
                choice = int(input("Enter the number you want to select: "))
                if 1 <= choice <= len(rooms):
                    selected_room = rooms[choice - 1][0]
                    print(f"You selected: room number: {selected_room.number}")
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                # Handle non-integer input
                print("Invalid input. Please enter a valid number.")
        return self

    def search_rooms(self, hotel_id):
        # Prompts the user to search for rooms based on various criteria
        print("Select the room type you want to search for:")
        print("1. Single Room")
        print("2. Double Room")
        print("3. Family Room")
        print("4. Suite")
        room_type_choice = input("Enter your choice (1-4 / Enter): ")

        room_type_dict = {
            "1": "single room",
            "2": "double room",
            "3": "family room",
            "4": "suite",
            "": "all",  # Default to 'all' if no choice is made
        }

        room_type = room_type_dict.get(room_type_choice, "all")
        if room_type == "all":
            room_type = None  # Treat 'all' as no specific room type

        max_guests = input("Enter the maximum number of guests you want to search for or press Enter for all: ")
        max_guests = int(max_guests) if max_guests.isdigit() and int(max_guests) > 0 else None

        price = input("Enter the price per night you want to search for or press Enter for all: ")
        price = int(price) if price.isdigit() and int(price) > 0 else None

        start_date = self.__validation_manager.input_start_date()
        end_date = self.__validation_manager.input_end_date(start_date) if start_date else None

        # If all inputs are skipped, display all rooms
        if not any([room_type, max_guests, price, start_date, end_date]):
            return self.display_all_rooms(hotel_id)

        query, rooms = self.get_desired_rooms_by_hotel_id(
            hotel_id, type=room_type, max_guests=max_guests,
            price=price, start_date=start_date, end_date=end_date
        )

        if not rooms:
            print("No rooms found matching the criteria.")
        else:
            print("\nAvailable rooms:")
            for index, room in enumerate(rooms, start=1):
                try:
                    hotel_name = self.get_hotel_name_by_id(room.Room.hotel_id)
                    room_info = (f"{index}. \033[4m{hotel_name}\033[0m\n"
                                 f"    Room Number: {room.Room.number}\n"
                                 f"    Type: {room.Room.type}\n"
                                 f"    Price per Night: {room.Room.price}\n")
                    print(room_info)
                    print("-" * 80)
                except AttributeError as e:
                    print(f"Error: {e}. Room attributes: {room._mapping}")

            try:
                choice = int(input("Enter the number you want to select: "))
                if 1 <= choice <= len(rooms):
                    selected_room = rooms[choice - 1].Room
                    Console.format_text(f"You selected: room number: {selected_room.number}")

                    # Ask if the user has a login
                    has_login = input("Do you have a login? (yes/no): ")
                    if has_login.lower() == 'yes':
                        # If the user has a login, retrieve the Guest instance associated with that login
                        username = input("Enter your username: ")
                        password = input("Enter your password: ")
                        guest = self._session.query(Guest).join(Login).filter(Login.username == username,
                                                                              Login.password == password).first()
                    else:
                        # If the user doesn't have a login, ask for their details and create a new Guest instance
                        firstname = input("Enter your first name: ")
                        lastname = input("Enter your last name: ")
                        email = input("Enter your email: ")
                        street = input("Enter your street and house number: ")
                        zip = input("Enter your zip code: ")
                        city = input("Enter your city: ")

                        address = Address(street=street, zip=zip, city=city)
                        self._session.add(address)
                        self._session.commit()

                        guest = Guest(firstname=firstname, lastname=lastname, email=email, address_id=address.id)
                        self._session.add(guest)
                        self._session.commit()

                    booking_manager = BookingManager()  
                    hotel_name = self.get_hotel_name_by_id(selected_room.hotel_id)
                    start_date = self.__validation_manager.input_start_date()
                    end_date = self.__validation_manager.input_end_date(start_date) if start_date else None

                    # Ask the user for the number of guests
                    number_of_guests = input("Enter the number of guests: ")
                    number_of_guests = int(number_of_guests) if number_of_guests.isdigit() else None

                    booking_manager.add_booking(hotel_name=hotel_name, start_date=start_date,
                                                end_date=end_date, hotel_id=selected_room.hotel_id,
                                                room_id=selected_room.number, guest_id=guest.id,
                                                number_of_guests=number_of_guests)
                else:
                    Console.format_text("Invalid selection. Please try again.")
            except ValueError:
                Console.format_text("Invalid input. Please enter a valid number.")
        return self

if __name__ == '__main__':
    # Set the database file path if not set in the environment
    if not os.environ.get('DB_FILE'):
        os.environ['DB_FILE'] = '../data/test.db'
    search_manager = SearchManager()
    all_hotels = search_manager.get_all_hotels()
    for hotel in all_hotels:
        print(hotel)