import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from business.BaseManager import BaseManager
from console.console_base import Console
from data_models.models import *
from business.ValidationManager import ValidationManager

class HotelManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        engine = create_engine(f'sqlite:///{os.environ.get("DB_FILE")}')
        Session = sessionmaker(bind=engine)
        self._session = Session()
        self.__validation_manager = ValidationManager()

    def get_session(self):
        return self

    def add_hotel(self): #adds hotel to the database
        print("Enter the following information")

        #variables
        streets = input(Console.format_text("Add hotel", "Enter street: "))
        city = input(Console.format_text("Add hotel", "Enter city: "))
        zip_code = self.__validation_manager.input_zip()
        hotel_name = input(Console.format_text("Add hotel", "Enter hotel name: "))
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

        # adds rooms in a loop
        def add_room(hotel_id):
            number = int(input(Console.format_text("Add hotel", "Enter room number: ")))
            type = input(Console.format_text("Add hotel", "Enter room type: "))
            max_guest = self.__validation_manager.room_max_guests(object)
            description = input(Console.format_text("Add hotel", "Enter a room description: "))
            amenities = input(Console.format_text("Add hotel", "Enter the amenities of the room: "))
            price = float(input(Console.format_text("Add hotel", "Enter the room price per night: ")))


            room = Room(hotel_id=hotel_id,
                        number= number,
                        type=type,
                        max_guests=max_guest,
                        description=description,
                        amenities=amenities,
                        price=price)
            self._session.add(room)
            self._session.commit()
            print("Room has been added to the database.")

        # Loop to add rooms
        while True:
            add_room(hotels.id)
            add_another = input("Do you want to add another room? (yes/no): ")
            if add_another != 'yes':
                print("All rooms have been added to the hotel.")
                break

    def delete_hotel(self): #deletes hotel from database
        #variables
        hotel_id = int(Console.format_text("delete hotel", "Enter hotel ID: "))
        hotel = self._session.query(Hotel).filter_by(id=hotel_id).first()

        if hotel:
            # Fetch and delete associated rooms
            room = self._session.query(Room).filter_by(hotel_id=hotel_id).all()
            for room in room:
                self._session.delete(room)
            # Delete the hotel
            self._session.delete(hotel)
            self._session.commit()
            print("Hotel and its associated rooms have been deleted from the database.")
        else:
            print("Invalid Hotel ID")

    def adjust_room(self, room): #method to edit room room information
        #variables
        room_number = int(input(Console.format_text("adjust room", "Enter room number: ")))
        room_type = input(Console.format_text("adjust room", "Enter room type: "))
        max_guest = self.__validation_manager.room_max_guests(object)
        room_description = input(Console.format_text("adjust room", "Enter a room description: "))
        room_amenities = input(Console.format_text("adjust room", "Enter the amenities of the room: "))
        room_price = float(input(Console.format_text("adjust room", "Enter the room price per night: ")))

        print("Adjusting room details. Press enter to skip.")
        #overrides the current information with the new information, if the there was an input
        room.number = room_number or room.number
        room.type = room_type or room.type
        room.max_guests = max_guest or room.max_guests
        room.description = room_description or room.description
        room.amenities = room_amenities or room.amenities
        room.price = room_price or room.price
        print("Room details have been updated.")

    def edit_hotel(self): #method to edit hotel information
        #variables
        current_hotel_name = input(Console.format_text("Edit Hotel", "Enter a hotel name: "))
        streets = input(Console.format_text("Edit hotel", "Enter street: "))
        city = input(Console.format_text("Edit hotel", "Enter city: "))
        zip_code = self.__validation_manager.input_zip()
        new_hotel_name = input(Console.format_text("Edit hotel", "Enter hotel name: "))
        stars = self.__validation_manager.input_star_rating()

        # Retrieve the hotel by name
        hotel = self._session.query(Hotel).filter_by(name=current_hotel_name).first()

        if not hotel:
            print(f"No hotel found with the name ' {current_hotel_name} '.")
            return
        # Retrieve the hotel address
        address = self._session.query(Address).filter_by(id=hotel.address_id).first()

        # Displays current hotel information
        print(f"Adjusting details for hotel: {hotel.name}")
        print(f"Current information for hotel:\n"
              f"Stars: {hotel.stars} \n"
              f"Street: {address.street} \n"
              f"Postal code: {address.zip} \n"
              f"City: {address.city}")
        # Adjust hotel details
        if input("Would you like to continue? (yes/no) :") == "yes":
            print("Adjusting details for hotel. Press enter to skip")
            hotel.name = new_hotel_name or hotel.name
            hotel.stars = stars or hotel.stars

            # Retrieve and adjust address details
            address.street = streets or address.street
            address.city = city or address.city
            address.zip = zip_code or address.zip

            self._session.commit()
            print("Hotel and address details have been updated.")
        else:
            print("Adjustment has been cancelled")
        #adjust room details if needed
        if input(Console.format_text("Edit hotel","Do you want to edit rooms (yes/no)")).strip().lower() == "yes":
            while True:
                room_number = input(Console.format_text("Edit room", "Enter the room number you want to adjust or type 'done' to finish): ")
                                    .strip().lower())
                if room_number == 'done':
                    break
                else:
                    room = self._session.query(Room).filter_by(hotel_id=hotel.id, number=room_number).first()
                    if not room:
                        print(f"No room found with the number '{room_number}' in this hotel.")
                        continue
                    #retrieves method to adjust hotel details
                    self.adjust_room(room)

    def edit_room(self): #method to edit room details
        #variables
        hotel_name = input(Console.format_text("Edit room", "In which hotel should the room be edited? "))
        hotel = self._session.query(Hotel).filter_by(name=hotel_name).first()
        if hotel:
            while True:  # Loop until valid room is selected
                room_number = int(input(Console.format_text("Edit room", "Enter room number to edit: ")))
                room = self._session.query(Room).filter_by(hotel_id=hotel.id, number=room_number).first()

                if room:
                    #trieves method to edit room details
                    self.adjust_room(room)
                    break
                else:
                    print("Room not found in this hotel. Please try again.")
        else:
            print("Hotel not found. Please try again.")

    def add_room(self): #adds room to a hotel
        #variables
        hotel_name = input(Console.format_text("Add room", "In which hotel should the room be added? "))
        room_number_ = int(input(Console.format_text("Add room", "Enter room number: ")))
        room_type_ = input(Console.format_text("Add room", "Enter room type: "))
        max_guest = self.__validation_manager.room_max_guests(object)
        room_description = input(Console.format_text("Add room", "Enter a room description: "))
        room_amenities = input(Console.format_text("Add room", "Enter the amenities of the room: "))
        room_price_ = float(input(Console.format_text("Add room", "Enter the room price per night: ")))

        hotel = self._session.query(Hotel).filter_by(name=hotel_name).first()
        if hotel:
            while True:
                try:
                    room_number = room_number_
                    # Check if the room number already exists in this hotel
                    existing_room = self._session.query(Room).filter_by(hotel_id=hotel.id, number=room_number).first()
                    if existing_room:
                        print(f"Room number {room_number} already exists in this hotel. Please choose another number.")
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

                    print("Room has been added to the database.")
                    break  # Exit the loop after successfully adding the room

                except ValueError:
                    print(
                        "Invalid input. Please check the inputs")
        else:
            print("Hotel not found. Please try again.")

    def delete_room(self): #deletes rooms from hotel
        #variables
        hotel_name = input(Console.format_text("Delete room", "In which hotel should the room be deleted? "))
        hotel = self._session.query(Hotel).filter_by(name=hotel_name).first()

        if not hotel:
            print(f"Hotel '{hotel_name}' not found.")
            return
        #checks if room exists
        while True:
            try:
                room_number = int(input(Console.format_text("Delete room", "Room number to delete: ")))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue  # Go back to the beginning of the loop

            room = self._session.query(Room).filter_by(hotel_id=hotel.id, number=room_number).first()

            #deletes room from database
            if room:
                self._session.delete(room)
                self._session.commit()
                print(f"Room {room_number} deleted from '{hotel_name}'.")
                break  # Exit the loop after successful deletion
            else:
                print(f"Room {room_number} not found in '{hotel_name}'.")
