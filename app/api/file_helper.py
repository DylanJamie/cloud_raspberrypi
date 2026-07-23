# file_helper.py

# functions needed for endpoints

# imports
from sqlmodel import Session, select
from passlib.context import CryptContext
from app.api.models import USER

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
def usr_logout():
    pass

# files
# Retrieve the files with in the users file system
# get all the file ids that the user owns
def usr_files():
    pass

# File augmentation
# download
# take the contents and download it to the local machine
def file_download():
    pass

# upload
# creating a new file class instance
# give it a file_id and owner_id (USER.user_id)
def file_upload():
    pass

# delete
# Remove that file instance from existance
def file_delete():
    pass

