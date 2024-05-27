import os
from sqlalchemy import select, func, text, create_engine
from sqlalchemy.orm import sessionmaker
from business.BaseManager import BaseManager
from data_models.models import *


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

    def get_hotels_by_name(self, name: str) -> List[Hotel]:
        query = select(Hotel).where(func.lower(Hotel.name).like(f"%{name.lower()}%"))
        return self.select_all(query)

    # 1.1.1. Ich möchte alle Hotels in einer Stadt durchsuchen, damit ich das Hotel nach meinem bevorzugten Standort (Stadt) auswählen kann.
    def get_hotels_by_city(self, city: str) -> List[Hotel]:
        query = select(Hotel).join(Address).where(Address.city == city)
        return self.select_all(query)

    def get_hotel_by_id(self, id: int) -> Hotel:
        query = select(Hotel).where(Hotel.id == id)
        return self.select_one(query)

    # 1.1.2. Ich möchte alle Hotels in einer Stadt nach der Anzahl der Sterne durchsuchen.
    # 1.1.3. Ich möchte alle Hotels in einer Stadt durchsuchen, die Zimmer haben, die meiner Gästezahl entsprechen (nur 1 Zimmer pro Buchung), entweder mit oder ohne Anzahl der Sterne.
    def search_hotels_by_city_and_max_guests_with_optional_star_rating(self, city, max_guests, stars=None):
        session = self.get_session()

        # Start of the SQL query
        query = """
            SELECT hotel.name, GROUP_CONCAT(room.number) as room_numbers
            FROM hotel
            JOIN address ON hotel.address_id = address.id
            JOIN room ON hotel.id = room.hotel_id
            WHERE address.city = :city
            AND room.max_guests >= :max_guests"""

        # If star_rating is specified, add it to the WHERE clause
        if stars is not None:
            query += " AND hotel.stars = :stars"

        # Add GROUP BY clause to avoid repeating hotel names
        query += " GROUP BY hotel.name"

        # Convert the query string to a SQLAlchemy text object
        query = text(query)

        # Execute the SQL query
        result = session.execute(query, {'city': city, 'max_guests': max_guests, 'stars': stars})

        # Fetch all the records
        hotels = result.fetchall()

        if not hotels:
            return 0

        # Format the output
        formatted_hotels = []
        for hotel in hotels:
            formatted_hotels.append(f"hotel_name: {hotel[0]}, room_numbers: {hotel[1]}")
        return formatted_hotels

    # 1.1.4. Ich möchte alle Hotels in einer Stadt durchsuchen, die während meines Aufenthaltes ("von" (start_date) und "bis" (end_date)) Zimmer für meine Gästezahl zur Verfügung haben, entweder mit oder ohne Anzahl der Sterne, damit ich nur relevante Ergebnisse sehe.
    # 1.1.5. Ich möchte die folgenden Informationen pro Hotel sehen: Name, Adresse, Anzahl der Sterne.
    # 1.1.6. Ich möchte ein Hotel auswählen, um die Details zu sehen (z.B.verfügbare Zimmer [siehe 1.2])


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
