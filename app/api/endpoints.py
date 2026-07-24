# endpoints.py

# imports
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Cookie, Response
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
def login(username: str, password: str, response: Response, session: Session = Depends(get_session)):
    user = file_helper.usr_login(username, password, session)

    # This means that the username or the password is wrong
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid Username or Password")

    # Create a new session for the user
    new_session = file_helper.create_session(user.user_id, session)

    # send the session id back as a cookie so future browsers send it
    response.set_cookie(key="session_id", value=new_session.session_id, httponly=True)
    
    # Session cookie logic comes out next
    return {"message": "login successful", "user_id": user.user_id} 
    

# clear the session ## FUTURE ADD A TIME OUT FOR USERS INACTIVE FOR a set amout of time
# POST Method
# /logout
@router.post("/logout")
def logout(response: Response, session_id: str = Cookie(default=None), session: Session = Depends(get_session)):
    if session_id:
        file_helper.usr_logout(session_id, session)
    response.delete_cookie("session_id")

    return {"message": "logged out"}

# list files for logged in user
# GET Method
# /files
@router.get("/files")
def files(owner_id: str, session: Session = Depends(get_session)):
    files = file_helper.usr_files(owner_id, session)

    return [
        {
            "file_id": f.file_id,
            "original_filename": f.original_filename,
            "content_type": f.content_type,
            "size_bytes": f.size_bytes,
            "uploaded_at": f.uploaded_at,
        }
        for f in files
    ]

# download a file
# GET method
# /files/{file_id}/download

# Upload a file
# POST Method
# /files/upload
@router.post("/files/upload")
def upload_file(file: UploadFile = File(...), owner_id: str = "", session: Session = Depends(get_session)):
    new_file = file_helper.file_upload(file, owner_id, session)

    return {
        "file_id": new_file.file_id,
        "original_filename": new_file.original_filename,
        "size_bytes": new_file.size_bytes
    }

# delete a file
# DELETE Method
# /files/delete

# confirm server is alive
# /GET Method
# /health
