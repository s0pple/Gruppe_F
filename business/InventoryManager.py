import os
from sqlalchemy import select, func, text, create_engine
from sqlalchemy.orm import sessionmaker
from business.BaseManager import *
from data_models.models import *


class HotelManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        Session = sessionmaker(bind=engine)
        self._session = Session()

    def get_session(self):
        return self

    def add_hotel(self, Hotel, Address, Room):
        print("Enter the following information")
        # adds address
        address = Address(street=str(input("Street:")),
                          city=str(input("City:")),
                          zip=int(input("Postal code:")))
        session.add(address)
        session.commit()
        print("Address has been added to the database. Address ID is", address.id)

        # Add new hotels with the addresses
        hotels = Hotel(name=str(input("Hotelname:")),
                       stars=int(input("Rating:")),
                       address_id=address.id)
        session.add(hotels)
        session.commit()
        print("Hotel has been added to the database. Hotel ID is", hotels.id)

        # adds rooms in a loop
        def add_room(hotel_id):
            room = Room(hotel_id=hotel_id,
                        number=int(input("Room number:")),
                        type=str(input("Room type:")),
                        max_guests=int(input("Maximum number of guests:")),
                        description=str(input("Description:")),
                        amenities=str(input("Amenities:")),
                        price=float(input("Room price:")))
            session.add(room)
            session.commit()
            print("Room has been added to the database.")

        # Loop to add rooms
        while True:
            add_room(hotels.id)
            add_another = input("Do you want to add another room? (yes/no): ")
            if add_another != 'yes':
                print("All rooms have been added to the hotel.")
                break

    def delete_hotel(self, Hotel, Room):
        hotel_id = int(input("Enter Hotel ID which will be deleted:"))
        hotel = session.query(Hotel).filter_by(id=hotel_id).first()
        if hotel:
            # Fetch and delete associated rooms
            room = session.query(Room).filter_by(hotel_id=hotel_id).all()
            for room in room:
                session.delete(room)
            # Delete the hotel
            session.delete(hotel)
            session.commit()
            print("Hotel and its associated rooms have been deleted from the database.")
        else:
            print("Invalid Hotel ID")

    def adjust_room(self, room):
        print("Adjusting room details. Press enter to skip.")
        room.number = int(input(f"Enter new room number (current: {room.number}): ")) or room.number
        room.type = str(input(f"Enter new room type (current: {room.type}): ")) or room.type
        room.max_guests = int(input(f"Enter new maximum number of guests (current: {room.max_guests}): ")) or room.max_guests
        room.description = str(input(f"Enter new description (current: {room.description}): ")) or room.description
        room.amenities = str(input(f"Enter new amenities (current: {room.amenities}): ")) or room.amenities
        room.price = float(input(f"Enter new room price (current: {room.price}): ")) or room.price
        session.commit()
        print("Room details have been updated.")

    def edit_hotel(self, Address, Hotel, Room):
        hotel_name = input("Enter the hotel name you want to adjust: ")

        # Retrieve the hotel by name
        hotel = session.query(Hotel).filter_by(name=hotel_name).first()

        if not hotel:
            print(f"No hotel found with the name ' {hotel_name} '.")
            return
        address = session.query(Address).filter_by(id=hotel.address_id).first()

        print(f"Adjusting details for hotel: {hotel.name}")
        print(f"Current information for hotel:\n"
              f"Stars: {hotel.stars} \n"
              f"Street: {address.street} \n"
              f"Postal code: {address.zip} \n"
              f"City: {address.city}")
        # Adjust hotel details
        if input("Would you like to continue? (yes/no) :") == "yes":
            print("Adjusting details for hotel. Press enter to skip")
            hotel.name = str(input(f"Enter new name for the hotel (current: {hotel.name}): ")) or hotel.name
            hotel.stars = int(input(f"Enter new rating for the hotel (current: {hotel.stars}): ")) or hotel.stars

            # Retrieve and adjust address details
            address.street = str(input(f"Enter new street (current: {address.street}): ")) or address.street
            address.city = str(input(f"Enter new city (current: {address.city}): ")) or address.city
            address.zip = int(input(f"Enter new postal code (current: {address.zip}): ")) or address.zip

            session.commit()
            print("Hotel and address details have been updated.")
        else:
            print("Adjustment has been cancelled")

        if input("Do you want to adjust the rooms? (yes/no): ").strip().lower() == "yes":
            while True:
                room_number = input(
                    "Enter the room number you want to adjust (or type 'add' to add a new room, 'done' to finish): ").strip().lower()
                if room_number == 'done':
                    break
                #elif room_number == 'add':
                 #   add_room_to_hotel(hotel.id, Room)
                else:
                    room = session.query(Room).filter_by(hotel_id=hotel.id, number=room_number).first()
                    if not room:
                        print(f"No room found with the number '{room_number}' in this hotel.")
                        continue
                    adjust_room(room)


#-----------------
add_hotel()