import os

from sqlalchemy import select, func

from business.BaseManager import BaseManager
from data_models.models import *


class SearchManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()

    def get_all_hotels(self) -> List[Hotel]:
        query = select(Hotel)
        return self.select_all(query)

    def get_hotels_by_name(self, name: str) -> List[Hotel]:
        query = select(Hotel).where(func.lower(Hotel.name).like(f"%{name.lower()}%"))
        return self.select_all(query)

    def get_hotels_by_city(self, city: str) -> List[Hotel]:
        query = select(Hotel).join(Address).where(Address.city == city)
        return self.select_all(query)

    def get_hotel_by_id(self, id: int) -> Hotel:
        query = select(Hotel).where(Hotel.id == id)
        return self.select_one(query)

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
