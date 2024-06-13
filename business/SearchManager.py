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
        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        Session = sessionmaker(bind=engine)
        self._session = Session()
        self.__validation_manager = ValidationManager()

    def get_session(self):
        return self._session

    def get_all_hotels(self) -> List[Hotel]:
        query = select(Hotel)
        return self.select_all(query)

    def get_hotel_name_by_id(self, hotel_id):
        query = select(Hotel.name).where(Hotel.id == hotel_id)
        result = self._session.execute(query).scalar_one()
        return result

    #
    # def get_hotels_by_name(self, name: str) -> List[Hotel]:
    #     query = select(Hotel).where(func.lower(Hotel.name).like(f"%{name.lower()}%"))
    #     return self.select_all(query)
    #
    # # 1.1.1. Ich möchte alle Hotels in einer Stadt durchsuchen, damit ich das Hotel nach meinem bevorzugten Standort (Stadt) auswählen kann.
    # def get_hotels_by_city(self, city: str) -> List[Hotel]:
    #     query = select(Hotel).join(Address).where(Address.city == city)
    #     return self.select_all(query)
    #
    # def get_hotel_by_id(self, id: int) -> Hotel:
    #     query = select(Hotel).where(Hotel.id == id)
    #     return self.select_one(query)
    #
    # # 1.1.2. Ich möchte alle Hotels in einer Stadt nach der Anzahl der Sterne durchsuchen.
    # # 1.1.3. Ich möchte alle Hotels in einer Stadt durchsuchen, die Zimmer haben, die meiner Gästezahl entsprechen (nur 1 Zimmer pro Buchung), entweder mit oder ohne Anzahl der Sterne.
    # def search_hotels_by_city_and_max_guests_with_optional_star_rating(self, city, max_guests, stars=None):
    #     session = self.get_session()
    #
    #     # Start of the SQL query
    #     query = """
    #         SELECT hotel.name, GROUP_CONCAT(room.number) as room_numbers
    #         FROM hotel
    #         JOIN address ON hotel.address_id = address.id
    #         JOIN room ON hotel.id = room.hotel_id
    #         WHERE address.city = :city
    #         AND room.max_guests >= :max_guests"""
    #
    #     # If star_rating is specified, add it to the WHERE clause
    #     if stars is not None:
    #         query += " AND hotel.stars = :stars"
    #
    #     # Add GROUP BY clause to avoid repeating hotel names
    #     query += " GROUP BY hotel.name"
    #
    #     # Convert the query string to a SQLAlchemy text object
    #     query = text(query)
    #
    #     # Execute the SQL query
    #     result = session.execute(query, {'city': city, 'max_guests': max_guests, 'stars': stars})
    #
    #     # Fetch all the records
    #     hotels = result.fetchall()
    #
    #     if not hotels:
    #         return 0
    #
    #     # Format the output
    #     formatted_hotels = []
    #     for hotel in hotels:
    #         formatted_hotels.append(f"hotel_name: {hotel[0]}, room_numbers: {hotel[1]}")
    #     return formatted_hotels

    # 1.1.4. Ich möchte alle Hotels in einer Stadt durchsuchen, die während meines Aufenthaltes ("von" (start_date) und "bis" (end_date)) Zimmer für meine Gästezahl zur Verfügung haben, entweder mit oder ohne Anzahl der Sterne, damit ich nur relevante Ergebnisse sehe.
    def get_hotels_by_city_guests_star_availability(self, hotel_name=None, city=None, max_guests=None, star_rating=None,
                                                    start_date=None,
                                                    end_date=None) -> List[Hotel]:
        query = select(Hotel)
        if hotel_name:
            query = query.where(Hotel.name.ilike(f"%{hotel_name}%"))
        if city:
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

        result = self._session.execute(query)
        # all_hotels = result.fetchall()
        # return all_hotels

        return self.select_all(query)  # , all_hotels

    # 1.1.5. Ich möchte die folgenden Informationen pro Hotel sehen: Name, Adresse, Anzahl der Sterne.
    # def display_hotel_info(self):
    #     all_hotels = self.get_all_hotels()
    #     hotels_info = []
    #     for hotel in all_hotels:
    #         hotel_info = f"Hotel Name: {hotel.name}\n"
    #         hotel_info += f"Address: {hotel.address.street}, {hotel.address.zip} {hotel.address.city}\n"
    #         hotel_info += f"Stars: {hotel.stars}\n"
    #         hotel_info += "-" * 50  # Separator for better readability
    #         hotels_info.append(hotel_info)
    #     return hotels_info

    # 1.1.6. Ich möchte ein Hotel auswählen, um die Details zu sehen (z.B.verfügbare Zimmer [siehe 1.2])

    # 1.2.1. Ich möchte die folgenden Informationen pro Zimmer sehen: Zimmertyp, max. Anzahl der Gäste, Beschreibung, Ausstattung, Preis pro Nacht und Gesamtpreis.
    # 1.2.2. Ich möchte nur die verfügbaren Zimmer sehen

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
        query, rooms = self.get_desired_rooms_by_hotel_id(hotel_id)
        if not rooms:
            print("No rooms found.")
        else:
            print("\nAvailable rooms:")
            for index, room in enumerate(rooms, start=1):
                room = room[0]
                hotel_name = self.get_hotel_name_by_id(room.hotel_id)  # Retrieve the hotel name
                room_info = (f"{index}. \033[4m[{hotel_name}]\033[0m\n"
                             f"    Room Number: {room.number}\n"
                             f"    Type: {room.type}\n"
                             f"    Price per Night: {room.price}\n")
                print(room_info)
                print("-" * 80)

            try:
                choice = int(input("Enter the number you want to select: "))
                if 1 <= choice <= len(rooms):
                    selected_room = rooms[choice - 1][0]
                    print(f"You selected: room number: {selected_room.number}")
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
            return self

    def search_rooms(self, hotel_id):
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
        max_guests = int(max_guests) if max_guests.isdigit() and 1 <= int(max_guests) <= 4 else None

        price = input("Enter the price per night you want to search for or press Enter for all: ")
        price = int(price) if price.isdigit() and int(price) > 0 else None

        start_date = self.__validation_manager.input_start_date()  # Replace get_start_date with input_start_date
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

                    booking_manager = BookingManager()  # Assuming you have a BookingManager class
                    hotel_name = self.get_hotel_name_by_id(selected_room.hotel_id)
                    start_date = self.__validation_manager.input_start_date()
                    if start_date is not None:
                        end_date = self.__validation_manager.input_end_date(start_date)
                    else:
                        end_date = None

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
    # This is only for testing without Application

    # You should set the variable in the run configuration
    # Because we are executing this file in the folder ./business/
    # we need to relatively navigate first one folder up and therefore,
    # use ../data in the path instead of ./data
    # if the environment variable is not set, set it to a default
    if not os.environ.get('DB_FILE'):
        os.environ['DB_FILE'] = '../data/test.db'
    search_manager = SearchManager()
    all_hotels = search_manager.get_all_hotels()
    for hotel in all_hotels:
        print(hotel)