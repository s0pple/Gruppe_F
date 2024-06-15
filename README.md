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
- Initializing and maintaining the database
- Updating the structure -> to the UE3 Classroom (scalability)
- 1 Guest User: 1.1 As a guest user, I want to search available hotels so that I can choose the one that meets my preferences. (with Patrick Nydegger)
- 1 Guest User: 1.2 As a guest user, I want to see details of different room types (single, double, family rooms) available in a hotel, including the maximum number of guests, description, price, and amenities, so that I can make an informed decision.
- Integration of external classes primarily the following; Menu(), SearchManager(), ValidationManager(), Session(), BaseManager() 
- UI / Menus & Submenus creation
- Creation of entity relationship diagram (ERD)
- Constructing the class diagram (old version was manually created, new version created with "instant reverse" and roughly added the missing classes, attributes, operations and relationships manually - we included both for contrast reasons)
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
- existing individual search functions combined and summarized, basic concept of building SQLAlchemy query (standard search and specification using “append”) defined, also for the other database interactions
- 1 Guest User: 1.6 As a guest user, I want to register with my email address and a personal identifier (password) to use additional functionalities (e.g., booking history, booking changes, etc. [see 2.1]).
- UI / Menus & Submenus creation
- concept and structure of the hotel reservation system with menu and submenu, definition of interactions between methods (with Vadivel Vaagisan, Schüpbach Michael , Haag Robin)
- construction and implementation of a validation manager to intercept incorrect and repetitive user entries

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

### All
- Mutual support when coding
- Weekly exchange and notification of work status, problems and challenges (every Sunday evening and Monday morning, and sometimes during the week)
- Extreme-coding-event on Saturday, June 01, 2024 09:30 am to 10:00 pm
  
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

**Main Menu**

The main menu is the first thing you'll see when you start the application. It provides several options for you to choose from. Here's a brief explanation of each option:

1. Search hotels with desired attributes:
   This option allows you to search for hotels based on specific attributes such as room type, maximum number of guests, price per night, and availability during a specific date range. After selecting this option, you'll be prompted to enter your desired attributes. If you want to skip any attribute, just press Enter without typing anything.  
3. User Menu:
   Here you get to the user menu, which deals with login and registration.
5. Quit:
   The program will be terminated.

To select an option, simply type the number of the option and press Enter.  

**Search Hotels**

When you select the "Search hotels with desired attributes" option, you'll be prompted to enter your desired attributes. Here's how you can do it:

 * no entry: If no entries are made for any of the following search options, all hotels from the database are displayed. The entries are complementary so that combinations are also possible.
   
You will now be asked for various search entries, all of which can be entered optionally. These entries are monitored so that incorrect entries can be restricted. For example, the number of stars can only have the values 1, 2, 3, 4 and 5.

  * end date(dd.mm.yyyy): This is only asked to be entered if a start date has been entered, but it is then mandatory to enter it.
    
if no hotels match the conditions, the entries are queried again with the message that no hotel was found.
Otherwise the hotels are listed and you can select one of them. The room search is started by the selection.

**Search Rooms**

After selecting the desired hotel you can choose one of the following options:

1. Search rooms in selected hotel
   *  Why: To find rooms based on specific criteria.
   * What next: Enter search criteria.
   * How: Enter room type, maximum number of guests, price per night (budget), and availability during a specific date range (you can also skip with Enter all the criterias you want to skip).
   * last step: View and select the room you want to book.

5. Display all available rooms
   * Why: To see all rooms without filters.
   * What next: View and select a room.
   * How: Only enter the start and end date of the desired stay or skip (press Enter) to show all.
   * last step: View and select the room you want to book.

9. Back
   * Why: To return to the main menu.
   * What next: Navigate to the previous menu.
   

***Book a Room***

When you see the list of available rooms, you can select a room to book. To select a room, simply type the number of the room and press Enter.

After selecting a room, you will be asked for your login:

- **Yes**: If you already have an account, enter your username and password.
- **No**: If you do not have an account, you can continue as a guest by entering your personal information.  
  *(Later on, you will still have the option to create an account.)*

Next, you will be able to enter a start and end date (dd.mm.yyyy) and the number of guests.

After entering your details, your booking will be confirmed, and you will see a confirmation message.

At the end, you will have the option to print out your booking.

- **Yes**: If you confirm, please check your Downloads folder in the Explorer on your device.
- **No**: If you exit as a guest, it will be impossible to check your booking later.

Remember, if you ever want to go back to the previous menu or exit the application, you can usually do so by selecting the "Back" or "Exit" option from the menu.

**User Menu**

1. Register:
   A new profile is written to the database by entering the e-mail and password and important user and address information. Many input conditions are checked and if the input is invalid, you will be asked to enter it again. After a successful registration you will be redirected to the user menu for login.
2. Login:
   In the login section, you are prompted to enter your registered email and password. 
   If the entered credentials match a user in the database, you are successfully logged in and redirected to the respective user menu (Registered User Menu or Admin Menu) based on your user role.
   If the entered credentials do not match any user in the database, you are informed about the unsuccessful login attempt and asked to try again or register a new account.
3. Main Menu:
   You return to the main menu.

**Registered User Menu**

Once you are logged in as a registered user, you will be redirected to the Registered User Menu. Here's a brief explanation of each option:

1. Show Bookings:
   This option allows you to view all your bookings. 
   When you select this option, a list of all your bookings will be displayed with details such as hotel name, room type, start date, end date, and booking status. 
   You can print out this list for your records by following the prompts after the list is displayed. 
   When you choose to print a booking, a text file with the booking details is created and saved in your Downloads folder.

2. Edit Booking:
   This option allows you to edit an existing booking. 
   When you select this option, you will be asked to enter the booking ID of the booking you want to edit. 
   Then, you can update the start date, end date, or cancel the booking.

3. Cancel Booking:
   This option allows you to cancel an existing booking. 
   When you select this option, you will be asked to enter the booking ID of the booking you want to cancel. 
   Once you confirm the cancellation, the booking will be removed from your bookings list.

4. Update User:
   This option allows you to update your user information. 
   When you select this option, you will be able to update your email, password, and other personal information.

5. Delete User:
   This option allows you to delete your user account, provided you have no future bookings. 
   When you select this option, you will be asked to confirm your decision. 
   Once confirmed, your user account and all associated bookings will be deleted.

6. Log Out:
   This option allows you to log out from your account. 
   When you select this option, you will be redirected back to the Main Menu.

7. Back:
   This option allows you to go back to the Main Menu.

To select an option, simply type the number of the option and press Enter. Please note that any changes you make to your bookings or user account are permanent and cannot be undone.

**Admin Menu**

Once you are logged in as an administrator, you will be redirected to the Admin Menu. Here's a brief explanation of each option:

1. Search Bookings:
   - This option allows you to view all bookings of a specific user.
   - When you select this option, you will be prompted to enter the user ID of the user whose bookings you want to view.
   - If the entered user ID is valid, a list of all bookings of the specified user will be displayed with details such as hotel name, room type, start date, end date, and booking status.

2. Edit Bookings:
   - This option allows you to edit any existing booking.
   - When you select this option, you will be asked to enter the booking ID of the booking you want to edit.
   - Then, you can update the start date, end date, or cancel the booking.

3. Cancel Bookings:
   - This option allows you to cancel any existing booking.
   - When you select this option, you will be asked to enter the booking ID of the booking you want to cancel.
   - Once you confirm the cancellation, the booking will be removed from the bookings list.

4. Hotel Panel:
   - This option redirects you to the Hotel Panel where you can manage hotel information.
   - In the Hotel Panel, you can add new hotels, update existing hotel information, or delete hotels.

5. Update User:
   - This option allows you to update any user's information.
   - When you select this option, you will be able to update a user's email, password, and other personal information.

6. Delete User:
   - This option allows you to delete any user account, provided they have no future bookings.
   - When you select this option, you will be asked to confirm your decision.
   - Once confirmed, the user account and all associated bookings will be deleted.

7. Logout:
   - This option allows you to log out from your account.
   - When you select this option, you will be redirected back to the Main Menu.

To select an option, simply type the number of the option and press Enter. Please note that any changes you make to bookings or user accounts are permanent and cannot be undone.


**END**

That's it! You should now be able to use the application effectively.

____________________________________________________________________________________________________________________

Artifacts: (for more information look inside the respective contribution)
- GitHub repository
- Code Convention - created with GitHub
- Kanban - created with GitHub
- Entity Relationship Diagram (ERD) - created with DBeaver
- Old Class Diagram VS New Class Diagram - created with Visual Paradigm
- BPMN - created with Camunda
- README File - created with PyCharm
- Code - created with PyCharm
- DataBase - created with PyCharm
- GUI - created with PowerPoint
