from data_access.data_base import get_db_connection
from sqlalchemy import text
# include all search functions here
# accept search criteria, search by various criteria

class SearchManager:

    def accept_search_criteria(self):
        criteria = []
        return criteria

    def show_available_hotels(self, criteria):
        pass

# 1.1.1. Ich möchte alle Hotels in einer Stadt durchsuchen, damit ich das Hotel nach meinem bevorzugten Standort (Stadt) auswählen kann.
    @staticmethod
    def search_hotels_by_city(database_path, city):
        session = get_db_connection(database_path)
        #connection = session.raw_connection()
        #cursor = connection.cursor()

        # Execute the SQL query
        query = text("""
            SELECT hotel.name
            FROM hotel
            JOIN address ON hotel.address_id = address.id
            WHERE address.city = :city""")
        result = session.execute(query, {'city': city})

        # Fetch all the records
        hotels = result.fetchall()
        return hotels

# 1.1.2. Ich möchte alle Hotels in einer Stadt nach der Anzahl der Sterne durchsuchen.
# 1.1.3. Ich möchte alle Hotels in einer Stadt durchsuchen, die Zimmer haben, die meiner Gästezahl entsprechen (nur 1 Zimmer pro Buchung), entweder mit oder ohne Anzahl der Sterne.
    @staticmethod
    def search_hotels_by_city_and_max_guests_with_optional_star_rating(database_path, city, max_guests, star_rating=None):
        session = get_db_connection(database_path)

        # Start of the SQL query
        query = """
            SELECT hotel.name, GROUP_CONCAT(room.number) as room_numbers
            FROM hotel
            JOIN address ON hotel.address_id = address.id
            JOIN room ON hotel.id = room.hotel_id
            WHERE address.city = :city
            AND room.max_guests >= :max_guests"""

        # If star_rating is specified, add it to the WHERE clause
        if star_rating is not None:
            query += " AND hotel.star_rating = :star_rating"

        # Add GROUP BY clause to avoid repeating hotel names
        query += " GROUP BY hotel.name"

        # Convert the query string to a SQLAlchemy text object
        query = text(query)

        # Execute the SQL query
        result = session.execute(query, {'city': city, 'max_guests': max_guests, 'star_rating': star_rating})

        # Fetch all the records
        hotels = result.fetchall()

        # Format the output
        formatted_hotels = []
        for hotel in hotels:
            formatted_hotels.append(f"hotel_name: {hotel[0]}, room_numbers: {hotel[1]}")
        return formatted_hotels

# 1.1.4. Ich möchte alle Hotels in einer Stadt durchsuchen, die während meines Aufenthaltes ("von" (start_date) und "bis" (end_date)) Zimmer für meine Gästezahl zur Verfügung haben, entweder mit oder ohne Anzahl der Sterne, damit ich nur relevante Ergebnisse sehe.
# 1.1.5. Ich möchte die folgenden Informationen pro Hotel sehen: Name, Adresse, Anzahl der Sterne.
# 1.1.6. Ich möchte ein Hotel auswählen, um die Details zu sehen (z.B.verfügbare Zimmer [siehe 1.2])