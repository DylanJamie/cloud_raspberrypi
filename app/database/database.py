# database.py

# import
from sqlmodel import SQLModel, Session, create_engine

# URL for the database
DATABASE_URL = "sqlite:///./cloud.db"

# create and start the engine for the database
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

# Create tables if they dont exist call once on start up
def init_db():
    SQLModel.metadata.create_all(engine)

# Dependency, this gives each request its own DB session
# this makes it so database request dont bleed into one another
# making it so 2 users cant hit the api at the same exact time
def get_session():
    with Session(engine) as session:
        yield session

# Create init database
# Admin and then user database
