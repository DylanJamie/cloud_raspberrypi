# file_helper.py

# functions needed for endpoints

# imports
from sqlmodel import Session, select
from passlib.context import CryptContext
from app.api.models import USER, FILE, SESSION
import hashlib
import os
from pathlib import Path

# Create base folder for all uploaded files
STORAGE_DIR = Path("storage")

# Password Encryption
# using bcrypt we can hash a little longer which protects us from attackers
# we can also add in rehashing and Two Factor Authentication in the future
# deprecated basically allows us to update our encryption methods in the future
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# register
# add a new user to the data base
# assign a user_id
# allow them to type an init username and pass
# later make them auto sign in or force them to the log in page
def usr_register(username: str, password: str, session: Session):
    # this will check to see if the username exists
    # the endpoint will send a 400 
    existing = session.exec(select(USER).where(USER.username == username)).first()
    if existing is not None:
        return None

    # Create a new user as long as there is not an existing user
    new_user = USER(
        username = username,
        password_hash = pwd_context.hash(password),
    )

    # Stage the user
    session.add(new_user)

    # commit the user to the disk (almost like a write)
    session.commit()

    # Sync the python object (USER Class) with what is now in the database and return to Endpoint
    session.refresh(new_user)
    return new_user

# Creating a session when ever a user logs in
# add the session to a new table within the database this will keep track of all the users that are logged in
def create_session(user_id: str, session: Session):
    new_session = SESSION(user_id=user_id)
    session.add(new_session)
    session.commit()
    session.refresh(new_session)
    
    return new_session

# login
# Grab and varify the user credentials
# First check to see if the user exists
# decrypt their password
# check to see if password is correct
# if correct show file system or home screen
def usr_login(username: str, password: str, session: Session):
    user = session.exec(select(USER).where(USER.username == username)).first()

    # endpoints.py will return 401 if user does not exist
    if not user:
        return None

    if not pwd_context.verify(password, user.password_hash):
        return None

    # if it passes both of these 
    return user
    
# logout
# end session for user_id thats logged in
def usr_logout(session_id: str, session: Session):
    existing_session = session.get(SESSION, session_id)
    if existing_session:
        session.delete(existing_session)
        session.commit()

# files
# Retrieve the files with in the users file system
# get all the file ids that the user owns
def usr_files(owner_id: str, session: Session):
    files = session.exec(select(FILE).where(FILE.owner_id == owner_id)).all()
    return files
    

# File augmentation
# download
# take the contents and download it to the local machine
def file_download():
    pass

# upload
# creating a new file class instance
# give it a file_id and owner_id (USER.user_id)
def file_upload(file, owner_id: str, session: Session):
    # we need to calculate the size of the file before it gets uploaded
    # we can use len() to measure it
    contents = file.file.read()
    size_bytes = len(contents)

    # hash the file to encrypt it (one way not reversable)
    file_hash = hashlib.sha256(contents).hexdigest()

    # Create the new file metadata row first so we get a file_id via uuid to name the file with
    new_file = FILE(
        owner_id=owner_id,
        original_filename=file.filename,
        storage_path="", # we can fill in the blank once we have a file_id
        content_type=file.content_type,
        file_hash=file_hash,
        size_bytes=size_bytes,
    )
    
    # Now we can build the path on the disk using the generated file id
    user_folder = STORAGE_DIR / owner_id
    user_folder.mkdir(parents=True, exist_ok=True)
    storage_path = user_folder / new_file.file_id
    new_file.storage_path = str(storage_path)

    # Actually write the bytes to disk
    with open(storage_path, "wb") as f:
        f.write(contents)

    # Now save the metadata toe to the data
    session.add(new_file)
    session.commit()
    session.refresh(new_file)

    return new_file
    
# delete
# Remove that file instance from existance
def file_delete():
    pass

