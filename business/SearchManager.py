import os
from sqlalchemy import select, create_engine, or_, and_
from sqlalchemy.orm import sessionmaker, aliased
from business.BaseManager import BaseManager
from data_models.models import *
from business.ValidationManager import ValidationManager
from console.console_base import Console
from sqlalchemy.orm import aliased


class SearchManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        # Setting up the database connection
        self.__select_hotel_menu = None
        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        session = sessionmaker(bind=engine)
        self._session = session()  # Initialize a session for database operations
        self.__validation_manager = ValidationManager()  # Initialize validation manager for input validation

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
        result = self._session.execute(query).scalar_one()  # Execute the query and return a single scalar result
        return result

    # Subquery to find booked room_hotel_id combinations
    def booking_subquery(self, start_date, end_date):
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

        return booking_subquery

    def get_hotels_by_city_guests_star_availability(self, hotel_name=None, city=None, max_guests=None, star_rating=None,
                                                    start_date=None,
                                                    end_date=None) -> List[Hotel]:

        # Start of building the query to get hotels with various optional filters
        query = select(Hotel).select_from(Hotel)

        # If hotel_name is specified, add it to the WHERE clause
        if hotel_name:
            # Filter by hotel name if provided
            query = query.where(Hotel.name.ilike(f"%{hotel_name}%"))

        # If city is specified, add it to the WHERE clause
        if city:
            # Join with Address table to filter by city
            query = query.join(Address, Hotel.address_id == Address.id).where(
                Address.city.ilike(f"%{city}%"))

        # If max_guests is specified, add it to the WHERE clause
        if max_guests:
            query = query.where(Hotel.rooms.any(max_guests <= Room.max_guests))

        # If star_rating is specified, add it to the WHERE clause
        if star_rating:
            query = query.where(Hotel.stars == star_rating)

        # If the start_date and end_date are specified, check availability
        if start_date and end_date:
            # Alias for the Booking table to avoid name conflicts

            booking_subquery = self.booking_subquery(start_date, end_date)

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

        # check whether hotels with the given attributes were found
        if not hotels:
            Console.format_text("No hotels were found.")
            input("Press Enter to continue...")
            return None
        else:
            Console.format_text("Available Hotels:")
            seen_hotel_names = set()  # workaround with set, so that the hotels are only displayed once
            for i, hotel in enumerate(hotels, start=1):
                if hotel.name not in seen_hotel_names:
                    Console.format_text(f"{i}: \033[4m{hotel.name}\033[0m\n"
                                        f"Address: {hotel.address.street}, {hotel.address.zip} {hotel.address.city}\n"
                                        f"Stars: {hotel.stars}")
                    seen_hotel_names.add(hotel.name)

            # Selection of the hotel
            while True:
                try:
                    choice = Console.format_text("To select the hotel of your choice ", "enter the number:").lower()
                    choice = int(choice)
                    if 1 <= choice <= len(hotels):

                        return choice  # Returns the user's choice if it is valid
                    else:
                        print("Invalid number. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

    def get_all_rooms_by_hotel_id(self, hotel_id):
        query = select(Room).where(Room.hotel_id == hotel_id)
        result = self._session.execute(query)
        all_rooms = result.scalars().all()
        return all_rooms

    def get_desired_rooms_by_hotel_id(self, hotel_id=None, number=None, type=None, max_guests=None, amenities=None,
                                      price=None, description=None, start_date=None, end_date=None) -> List[Room]:
        # Start by creating a basic query to select all rooms
        query = select(Room)

        # Filter the query based on the provided criteria
        if hotel_id:
            query = query.where(Room.hotel_id == hotel_id)
        if number:
            query = query.where(Room.number == number)
        if type:
            query = query.where(Room.type == type)
        if max_guests:
            query = query.where(Room.max_guests == max_guests)
        if price:
            query = query.where(Room.price <= price)

        # Get the start and end dates for the booking period
        start_date = self.__validation_manager.input_start_date()
        if start_date is not None:
            end_date = self.__validation_manager.input_end_date(start_date)
        else:
            end_date = None

        # If both start and end dates are provided, filter out booked rooms during this period
        if start_date and end_date:
            # Subquery to find rooms that are already booked during the given period
            booking_subquery = self.booking_subquery(start_date, end_date)

            # Main query to exclude hotels with booked rooms during the requested period
            query = query.outerjoin(
                booking_subquery,
                and_(
                    Room.hotel_id == booking_subquery.c.room_hotel_id,
                    Room.number == booking_subquery.c.room_number
                )
            ).where(booking_subquery.c.room_hotel_id == None).group_by(Room.number)

        # Execute the query and fetch all results
        result = self._session.execute(query)
        all_rooms = result.fetchall()
        return self.select_all(query), all_rooms

    def display_all_rooms(self, hotel_id):
        from business.BookingManager import BookingManager
        # Display all rooms for a specific hotel
        query, rooms = self.get_desired_rooms_by_hotel_id(hotel_id)

        if not rooms:
            Console.format_text("No rooms found.")
        else:
            Console.format_text("Available rooms:")
            for index, room in enumerate(rooms, start=1):
                room = room[0]  # Fetch the room details from the query result
                hotel_name = self.get_hotel_name_by_id(room.hotel_id)  # Retrieve the hotel name
                room_info = (f"{index}. \033[4m{hotel_name}\033[0m\n"
                             f"    Room Number: {room.number}\n"
                             f"    Type: {room.type}\n"
                             f"    Price per Night: {room.price}")
                Console.format_text(room_info)

        try:
            choice = int(input("Enter the number you want to book: "))
            if 1 <= choice <= len(rooms):
                selected_room = rooms[choice - 1].Room
                Console.format_text(f"You selected the following room number for booking: {selected_room.number}")

                has_login = Console.format_text("Login", "Do you have a login? (yes/no): ").strip().lower()
                if has_login == 'yes':
                    # If the user has a login, retrieve the Guest instance associated with that login
                    username = Console.format_text("Login", "Enter your username: ").strip()
                    password = Console.format_text("Login", "Enter your password: ").strip()
                    registered_guest_alias = aliased(RegisteredGuest, flat=True)

                    guest = self._session.query(Guest).join(registered_guest_alias).join(Login).filter(
                        Guest.email == username, Login.password == password).first()
                else:
                    # If the user doesn't have a login, ask for their details and create a new Guest instance
                    firstname = Console.format_text("Guest Details", "Enter your first name: ").strip()
                    lastname = Console.format_text("Guest Details", "Enter your last name: ").strip()
                    email = Console.format_text("Guest Details", "Enter your email: ").strip()
                    street = Console.format_text("Guest Details", "Enter your street and house number: ").strip()
                    zip = Console.format_text("Guest Details", "Enter your zip code: ").strip()
                    city = Console.format_text("Guest Details", "Enter your city: ").strip()

                    address = Address(street=street, zip=zip, city=city)
                    self._session.add(address)
                    self._session.commit()

                    guest = Guest(firstname=firstname, lastname=lastname, email=email, address_id=address.id)
                    self._session.add(guest)
                    self._session.commit()

                    # Ask the guest if they want to create an account
                    create_account = Console.format_text("Account Creation",
                                                         "Do you want to create an account? (yes/no): ").strip().lower()
                    if create_account == 'yes':
                        username = email
                        self.__validation_manager.create_password(username)

                booking_manager = BookingManager()
                hotel_name = self.get_hotel_name_by_id(selected_room.hotel_id)
                start_date = self.__validation_manager.input_start_date()
                end_date = self.__validation_manager.input_end_date(start_date) if start_date else None

                number_of_guests = input("Enter the number of guests: ").strip()
                number_of_guests = int(number_of_guests) if number_of_guests.isdigit() else None

                booking_manager.add_booking(
                    hotel_name=hotel_name,
                    start_date=start_date,
                    end_date=end_date,
                    hotel_id=selected_room.hotel_id,
                    room_id=selected_room.number,
                    guest_id=guest.id,
                    number_of_guests=number_of_guests
                )
            else:
                Console.format_text("Invalid selection. Please try again.")
        except ValueError:
            Console.format_text("Invalid input. Please enter a valid number.")
        return self

    def search_rooms(self, hotel_id):
        from business.BookingManager import BookingManager  #Lazy import

        # Prompts the user to search for rooms based on various criteria
        Console.format_text("Select the room type you want to search for:")
        print("1. Single Room")
        print("2. Double Room")
        print("3. Family Room")
        print("4. Suite")
        print("Enter. for all room types")
        print("******************************************************************************************")
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
            room_type = None  # Treat "all" as no specific room type

        max_guests = self.__validation_manager.input_max_guests()

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

        # Debugging statement to check rooms list
        print(f"Rooms found: {rooms}")

        # Should check if the rooms list is empty, but somehow does not display the message
        # (when emulate run option turned off, then it shows the message)
        if not rooms:
            Console.format_text("No rooms found matching the criteria.")
        else:
            Console.format_text("Available rooms:")
            for index, room in enumerate(rooms, start=1):
                try:
                    hotel_name = self.get_hotel_name_by_id(room.Room.hotel_id)
                    room_info = (f"{index}. \033[4m{hotel_name}\033[0m\n"
                                 f"   Room Number: {room.Room.number}\n"
                                 f"   Type: {room.Room.type}\n"
                                 f"   Price per Night: {room.Room.price}")
                    Console.format_text(room_info)
                except AttributeError as e:
                    Console.format_text(f"Error: {e}. Room attributes: {room._mapping}")

            try:
                choice = int(input("Enter the number you want to book: "))
                if 1 <= choice <= len(rooms):
                    selected_room = rooms[choice - 1].Room
                    Console.format_text(f"You selected the following room number for booking: {selected_room.number}")

                    has_login = Console.format_text("Login", "Do you have a login? (yes/no): ").strip().lower()
                    if has_login == 'yes':
                        # If the user has a login, retrieve the Guest instance associated with that login
                        username = Console.format_text("Login", "Enter your username: ").strip()
                        password = Console.format_text("Login", "Enter your password: ").strip()
                        registered_guest_alias = aliased(RegisteredGuest, flat=True)

                        guest = self._session.query(Guest).join(registered_guest_alias).join(Login).filter(
                            Guest.email == username, Login.password == password).first()
                    else:
                        # If the user doesn't have a login, ask for their details and create a new Guest instance
                        firstname = Console.format_text("Guest Details", "Enter your first name: ").strip()
                        lastname = Console.format_text("Guest Details", "Enter your last name: ").strip()
                        email = Console.format_text("Guest Details", "Enter your email: ").strip()
                        street = Console.format_text("Guest Details", "Enter your street and house number: ").strip()
                        zip = Console.format_text("Guest Details", "Enter your zip code: ").strip()
                        city = Console.format_text("Guest Details", "Enter your city: ").strip()

                        address = Address(street=street, zip=zip, city=city)
                        self._session.add(address)
                        self._session.commit()

                        guest = Guest(firstname=firstname, lastname=lastname, email=email, address_id=address.id)
                        self._session.add(guest)
                        self._session.commit()

                        # Ask the guest if they want to create an account
                        create_account = Console.format_text("Account Creation",
                                                             "Do you want to create an account? (yes/no): ").strip().lower()
                        if create_account == 'yes':
                            username = email
                            self.__validation_manager.create_password(username)

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
    if not os.environ.get('DB_FILE'):
        os.environ['DB_FILE'] = '../data/test.db'
    search_manager = SearchManager()
    all_hotels = search_manager.get_all_hotels()
    for hotel in all_hotels:
        print(hotel)
