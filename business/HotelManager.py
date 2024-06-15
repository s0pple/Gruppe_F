import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from business.BaseManager import BaseManager
from console.console_base import Console
from data_models.models import *
from business.ValidationManager import ValidationManager


class HotelManager(BaseManager):
    def __init__(self, hotel_menu) -> None:
        super().__init__()
        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        session = sessionmaker(bind=engine)
        self._session = session()
        self.__validation_manager = ValidationManager()
        self.hotel_menu = hotel_menu
    # Add this line

    def get_session(self):
        return self

    def add_hotel(self):  #adds hotel to the database
        print("Enter the following information")

        #variables
        streets = Console.format_text("Add hotel", "Enter street: ")
        city = Console.format_text("Add hotel", "Enter city: ")
        zip_code = self.__validation_manager.input_zip()
        hotel_name = Console.format_text("Add hotel", "Enter hotel name: ")
        stars = self.__validation_manager.input_star_rating()

        # adds address
        address = Address(street=streets,
                          city=city,
                          zip=zip_code)
        self._session.add(address)
        self._session.commit()
        print("Address has been added to the database. Address ID is", address.id)

        # Add new hotels with the addresses
        hotels = Hotel(name=hotel_name,
                       stars=stars,
                       address_id=address.id)
        self._session.add(hotels)
        self._session.commit()
        print("Hotel has been added to the database. Hotel ID is", hotels.id)
        return self.hotel_menu

    def add_room(self, hotel_id):
        number = (input(Console.format_text("Add hotel", "Enter room number: ")))
        room_type = input(Console.format_text("Add hotel", "Enter room type: "))
        max_guest = input(Console.format_text("Add room", "Enter maximum guest allowed in this room: "))
        description = input(Console.format_text("Add hotel", "Enter a room description: "))
        amenities = input(Console.format_text("Add hotel", "Enter the amenities of the room: "))
        price = (input(Console.format_text("Add hotel", "Enter the room price per night: ")))

        room = Room(hotel_id=hotel_id,
                    number=number,
                    type=room_type,
                    max_guests=max_guest,
                    description=description,
                    amenities=amenities,
                    price=price)
        self._session.add(room)
        self._session.commit()
        Console.format_text("Room has been added to the database.")
        return self.hotel_menu

    def delete_hotel(self):  #deletes hotel from database
        #variables
        hotel_id = Console.format_text("delete hotel", "Enter hotel ID: ")
        hotel = self._session.query(Hotel).filter_by(id=hotel_id).first()

        if hotel:
            # Fetch and delete associated rooms
            room = self._session.query(Room).filter_by(hotel_id=hotel_id).all()
            for room in room:
                self._session.delete(room)
            # Delete the hotel
            self._session.delete(hotel)
            self._session.commit()
            Console.format_text("Hotel and its associated rooms have been deleted from the database.")
        else:
            Console.format_text("Invalid Hotel ID")
            return self.hotel_menu

    def adjust_room(self, room):  #method to edit room room information
        #variables
        room_number = Console.format_text("adjust room", "Enter room number: ")
        room_type = Console.format_text("adjust room", "Enter room type: ")
        max_guest = Console.format_text("Add room", "Enter maximum guest allowed in this room: ")
        room_description = Console.format_text("adjust room", "Enter a room description: ")
        room_amenities = Console.format_text("adjust room", "Enter the amenities of the room: ")
        room_price = Console.format_text("adjust room", "Enter the room price per night: ")

        Console.format_text("Adjusting room details. Press enter to skip.")
        #overrides the current information with the new information, if the there was an input
        room.number = room_number or room.number
        room.type = room_type or room.type
        room.max_guests = max_guest or room.max_guests
        room.description = room_description or room.description
        room.amenities = room_amenities or room.amenities
        room.price = room_price or room.price
        Console.format_text("Room details have been updated.")
        return self.hotel_menu

    def edit_hotel(self):  #method to edit hotel information
        #variables
        current_hotel_name = Console.format_text("Edit Hotel", "Enter a hotel name: ")
        streets = Console.format_text("Edit hotel", "Enter street: ")
        city = Console.format_text("Edit hotel", "Enter city: ")
        new_hotel_name = Console.format_text("Edit hotel", "Enter hotel name: ")
        stars = self.__validation_manager.input_star_rating()

        # Retrieve the hotel by name
        hotel = self._session.query(Hotel).filter_by(name=current_hotel_name).first()

        if not hotel:
            print(f"No hotel found with the name ' {current_hotel_name} '.")
            return
        # Retrieve the hotel address
        address = self._session.query(Address).filter_by(id=hotel.address_id).first()

        # Displays current hotel information
        Console.format_text(f"Adjusting details for hotel: {hotel.name}")
        Console.format_text(f"Current information for hotel:\n"
              f"Stars: {hotel.stars} \n"
              f"Street: {address.street} \n"
              f"Postal code: {address.zip} \n"
              f"City: {address.city}")
        # Adjust hotel details
        if Console.format_text("Edit Hotel", "Would you like to continue? (yes/no) :") == "yes":
            Console.format_text("Adjusting details for hotel. Press enter to skip")
            hotel.name = new_hotel_name or hotel.name
            hotel.stars = stars or hotel.stars

            # Retrieve and adjust address details
            address.street = streets or address.street
            address.city = city or address.city
            address.zip = address.zip

            self._session.commit()
            Console.format_text("Hotel and address details have been updated.")
        else:
            Console.format_text("Adjustment has been cancelled")
        #adjust room details if needed
        if Console.format_text("Edit hotel", "Do you want to edit rooms (yes/no)").strip().lower() == "yes":
            while True:
                room_number = Console.format_text(
                    "Edit room",
                    "Enter the room number you want to adjust or type 'done' to finish): "
                ).strip().lower()
                if room_number == 'done':
                    break
                else:
                    room = self._session.query(Room).filter_by(hotel_id=hotel.id, number=room_number).first()
                    if not room:
                        Console.format_text(f"No room found with the number '{room_number}' in this hotel.")
                        continue
                    #retrieves method to adjust hotel details
                    self.adjust_room(room)
                    return self.hotel_menu

    def edit_room(self):  #method to edit room details
        #variables
        hotel_name = Console.format_text("Edit room", "In which hotel should the room be edited? ")
        hotel = self._session.query(Hotel).filter_by(name=hotel_name).first()
        if hotel:
            while True:  # Loop until valid room is selected
                room_number_prompt = Console.format_text("Edit room", "Enter room number to edit: ")
                room_number = int(input(room_number_prompt))
                room = self._session.query(Room).filter_by(hotel_id=hotel.id, number=room_number).first()

                if room:
                    #trieves method to edit room details
                    self.adjust_room(room)
                    break
                else:
                    Console.format_text("Room not found in this hotel. Please try again.")
        else:
            Console.format_text("Hotel not found. Please try again.")

        return self.hotel_menu

    def add_room(self):  #adds room to a hotel
        #variables
        hotel_name = Console.format_text("Add room", "In which hotel should the room be added? ")
        room_number_ = Console.format_text("Add room", "Enter room number: ")
        room_type_ = Console.format_text("Add room", "Enter room type: ")
        max_guest = Console.format_text("Add room", "Enter maximum guest allowed in this room: ")
        room_description = Console.format_text("Add room", "Enter a room description: ")
        room_amenities = Console.format_text("Add room", "Enter the amenities of the room: ")
        room_price_ = Console.format_text("Add room", "Enter the room price per night: ")

        hotel = self._session.query(Hotel).filter_by(name=hotel_name).first()
        if hotel:
            while True:
                try:
                    room_number = room_number_
                    # Check if the room number already exists in this hotel
                    existing_room = self._session.query(Room).filter_by(hotel_id=hotel.id, number=room_number).first()
                    if existing_room:
                        Console.format_text(f"Room number {room_number} already exists in this hotel."
                                            f" Please choose another number.")
                        continue  # Go back to the beginning of the loop

                    # Get input for the new room's details
                    room_type = room_type_
                    max_guests = max_guest
                    description = room_description
                    amenities = room_amenities
                    room_price = room_price_

                    # Create and add the new room
                    new_room = Room(
                        hotel_id=hotel.id,
                        number=room_number,
                        type=room_type,
                        max_guests=max_guests,
                        description=description,
                        amenities=amenities,
                        price=room_price
                    )
                    self._session.add(new_room)
                    self._session.commit()

                    Console.format_text("Room has been added to the database.")
                    break  # Exit the loop after successfully adding the room

                except ValueError:
                    Console.format_text("Invalid input. Please check the inputs")
        else:
            Console.format_text("Hotel not found. Please try again.")
        return self.hotel_menu

    def delete_room(self):
        hotel_name = Console.format_text("Delete room", "In which hotel should the room be deleted? ")
        hotel = self._session.query(Hotel).filter_by(name=hotel_name).first()

        if not hotel:
            Console.format_text("Hotel '{hotel_name}' not found.")
            return

        while True:
            try:
                room_nr = Console.format_text("Delete room", "Room number to delete: ")
            except ValueError:
                Console.format_text("Invalid input. Please enter a number.")
                continue  # Go back to the beginning of the loop

            room = self._session.query(Room).filter_by(hotel_id=hotel.id, number=room_nr).first()

            if room:
                self._session.delete(room)
                self._session.commit()
                Console.format_text(f"Room {room_nr} deleted from '{hotel_name}'.")
                break  # Exit the loop after successful deletion
            else:
                Console.format_text(f"Room {room_nr} not found in '{hotel_name}'.")
            return self.hotel_menu
