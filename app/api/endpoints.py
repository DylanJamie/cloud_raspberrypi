# endpoints.py

# imports
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database.database import get_session
from app.api import file_helper

# application instance
router = APIRouter()

# Create an account
# POST Method
# /register
@router.post("/register")
def register(username: str, password:str, session: Session = Depends(get_session)):
    user = file_helper.usr_register(username, password, session)

    # check to see if there is no error with the username
    if user is None:
        raise HTTPException(status_code=400, detail="Username already taken")

    return {"user_id": user.user_id, "username": user.username} 
    
# authentication for users and set the session cookies
# POST Method
# /login
@router.post("/login")
def login(username: str, password: str, session: Session = Depends(get_session)):
    user = file_helper.usr_login(username, password, session)

    # This means that the username or the password is wrong
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid Username or Password")
    
    # Session cookie logic comes out next
    return {"message": "login successful", "user_id": user.user_id} 
    

# clear the session
# POST Method
# /logout

# list files for logged in user
# GET Method
# /files

# download a file
# GET method
# /files/{file_id}/download

# Upload a file
# POST Method
# /files/upload

# delete a file
# DELETE Method
# /files/delete

# confirm server is alive
# /GET Method
# /health
