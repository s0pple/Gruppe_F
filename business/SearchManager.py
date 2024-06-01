import os
from sqlalchemy import select, func, text, create_engine, or_, and_
from sqlalchemy.orm import sessionmaker, aliased
from business.BaseManager import BaseManager
from data_models.models import *
from datetime import datetime

class SearchManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        Session = sessionmaker(bind=engine)
        self._session = Session()

    def get_session(self):
        return self._session

    def get_all_hotels(self) -> List[Hotel]:
        query = select(Hotel)
        return self.select_all(query)

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
    def get_desired_rooms_by_hotel_id(self, hotel_id=None, number=None, type=None, max_guests=None, amenities=None,
                                      price=None, start_date=None, end_date=None, description=None) -> List[Room]:
        query = select(Room).where(Room.available == True)  # Only select available rooms

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
            query = query.where(Room.price == price)

        if description:
            query = query.where(Room.description == description)

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

    def get_hotel_name_by_id(self, hotel_id):
        query = select(Hotel.name).where(Hotel.id == hotel_id)
        result = self._session.execute(query).scalar_one()
        return result


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



