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