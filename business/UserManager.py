# imports
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session
from data_access.data_base import init_db
from data_models.models import *

# structure for SQAlchemy
if __name__ == '__main__':
    database_file = "./data/hotel_reservation.db"

    database_path = Path(database_file)
    if not database_path.parent.exists():
        database_path.parent.mkdir()

    # Tells SQAlchemy how to connect to the db.
    engine = create_engine(f'sqlite:///{database_path}', echo=False)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    init_db(database_file, generate_example_data=True)

    # Let's create a session to connect to the db.
    session = scoped_session(sessionmaker(bind=engine))

# creates a session to connect to the db.
session = scoped_session(sessionmaker(bind=engine))


def register_user():
    login = [Login(username=input("Username: "), password=input("Password: "), role_id=int(input("Role: ")))]
    for login in login:
        session.add(login)

    session.commit()
    print("login has been added to the database. Address ID is")


# login()
register_user()

print("All login as objects:")
query = select(Login)
result = session.execute(query).scalars().all()
for Login in result:
    print(Login)
