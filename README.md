# Groupe F

## Team Members
- **Gwerder Oliver**
- **Haag Robin**
- **Nydegger Patrick**
- **Schüpbach Michael**
- **Vadivel Vaagisan**

## Project Description
Welcome to Group F's project for the module "Application Development with Python" in the BSc BAI program. This module involves project-based learning of programming concepts using Python. Our project is centered around developing a hotel reservation system, a practical application scenario where we progressively apply programming concepts taught throughout the course.

This project has been a collaborative effort, reflecting the contributions and teamwork of each member of Group F. Together, we have navigated through various stages of development, tackling user stories to build a functional and user-friendly hotel reservation system. From initial planning and coding to testing and refining, we've aimed to integrate both foundational and advanced programming techniques in Python.

## Contributions of Team Members

### Gwerder Oliver
- Initializing GitHub repository
- Registering GitHub Premium & integrating with PyCharm
- Updating the structure -> to the UE3 Classroom (scalability)
- 1 Guest User: 1.1 As a guest user, I want to search available hotels so that I can choose the one that meets my preferences. (with Patrick Nydegger)
- 1 Guest User: 1.2 As a guest user, I want to see details of different room types (single, double, family rooms) available in a hotel, including the maximum number of guests, description, price, and amenities, so that I can make an informed decision.
- UI / Menus & Submenus creation
- Creating the README.md file

### Haag Robin
- Registering GitHub Premium & integrating with PyCharm
- Setting up the project with GitHub Desktop
- 2 Registered: 2.1 As a registered user, I want to log into my account to access my booking history ("read"), so that I can manage my upcoming reservations.
- 3 Admin: 3.2 As an admin user of the booking system, I want to see all bookings of all hotels to get an overview.
- 3 Admin: 3.3 I want to edit all bookings to add missing information (e.g., phone number)
- UI / Menus & Submenus creation
- Contributed to UserMenu, AdminMenu, RegisteredUserMenu, UserManager, BookingManager, Validation Manager, UI Implementation
- Modelled the AdminMenu and Registered User Menu

### Nydegger Patrick
- Registering GitHub Premium & integrating with PyCharm
- Converting user stories into BPMN processes
- 1 Guest User: 1.1 As a guest user, I want to search available hotels so that I can choose the one that meets my preferences. (with Oliver Gwerder)
- 1 Guest User: 1.6 As a guest user, I want to register with my email address and a personal identifier (password) to use additional functionalities (e.g., booking history, booking changes, etc. [see 2.1]).
- UI / Menus & Submenus creation

### Schüpbach Michael
- Registering GitHub Premium & integrating with PyCharm
- Creating code conventions (in Markdown file)
- 1 Guest User: 1.3 As a guest user, I want to book a room in a specific hotel to plan my vacation.
- 1 Guest User: 1.5 As a guest user, I want to receive the details of my reservation in a readable form (e.g., save the reservation in a permanent file) so that I can review my booking later.
- 3 Admin: 3.1 As an admin user of the booking system, I want to be able to maintain hotel information to keep the system up-to-date. (with Vadivel Vaagisan)
- UI / Menus & Submenus creation

### Vadivel Vaagisan
- Registering GitHub Premium & integrating with PyCharm
- Setting up Kanban
- 3 Admin: 3.1 As an admin user of the booking system, I want to be able to maintain hotel information to keep the system up-to-date. (with Michael Schüpbach)
- GUI as a PPTX file
- Modelled the AdminMenu and Registered User Menu 

## Using the Application

### Step-by-Step Guide

1. **Clone the Repository** -
First, you need to clone the repository to your local machine. You can do this by using the following command in your terminal:
   ```bash
   git clone https://github.com/s0pple/Gruppe_F.git
   cd Gruppe_F

2. **Create and Activate a Virtual Environment** -
Next, you should create a virtual environment for the project. This helps to keep the project's dependencies isolated from other Python projects on your machine. Here's how you can do it:

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS and Linux
   python3 -m venv venv
   source venv/bin/activate

3. **Install Dependencies** -
After activating the virtual environment, you need to install the project's dependencies. These are listed in the requirements.txt file. You can install them using pip:

   ```bash
   pip install -r requirements.txt
   
4. **Initialize the Database** -
Before you can run the application, you need to initialize the database. This can be done by running the init_db function from the data_access/data_base.py file. Please ensure that you provide the correct path to the SQLite database file.

   ```bash
   from data_access.data_base import init_db

   init_db('path_to_your_database_file')

5. **Run the Application** -
Finally, you can run the application. This can be done by running the main.py file:

   ```bash
   python main.py

6. **Use the Application** -
Once the application is running, you will see a command-line interface with various options. Here's how you can interact with it:  

***Main Menu***

The main menu is the first thing you'll see when you start the application. It provides several options for you to choose from. Here's a brief explanation of each option:

1. Search hotels with desired attributes: This option allows you to search for hotels based on specific attributes such as room type, maximum number of guests, price per night, and availability during a specific date range. After selecting this option, you'll be prompted to enter your desired attributes. If you want to skip any attribute, just press Enter without typing anything.  
2. Back: This option allows you to go back to the previous menu. If you're already at the main menu, selecting this option will exit the application.  

To select an option, simply type the number of the option and press Enter.  

***Search Hotels***

When you select the "Search hotels with desired attributes" option, you'll be prompted to enter your desired attributes. Here's how you can do it:

1. Select the room type: You'll see a list of room types to choose from. Type the number of your desired room type and press Enter. If you want to search for all room types, just press Enter without typing anything.  
2. Enter the maximum number of guests: Type the maximum number of guests you want to search for and press Enter. If you want to search for all numbers of guests, just press Enter without typing anything.  
3. Enter the price per night: Type the price per night you want to search for and press Enter. If you want to search for all prices, just press Enter without typing anything.  
4. Enter the start and end dates: You'll be prompted to enter the start and end dates of your stay. Type the dates in the format DD-MM-YYYY and press Enter. If you want to search for all dates, just press Enter without typing anything.  

After entering your desired attributes, the application will display a list of hotels that match your criteria. You can then select a hotel to see more details.  

***Select a Hotel***

When you see the list of hotels, you can select a hotel to see more details. To select a hotel, simply type the number of the hotel and press Enter.

Once you've selected a hotel, you'll see a list of available rooms in that hotel. You can then select a room to book.  

***Book a Room***

When you see the list of available rooms, you can select a room to book. To select a room, simply type the number of the room and press Enter.

After selecting a room, you'll be prompted to enter your booking details such as your name and contact information. After entering your details, your booking will be confirmed, and you'll see a confirmation message.

Remember, if you ever want to go back to the previous menu or exit the application, you can usually do so by selecting the "Back" or "Exit" option from the menu.  



**END**

That's it! You should now be able to use the application effectively.