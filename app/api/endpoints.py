# endpoints.py

# imports
from fastapi import APIRouter

# application instance
router = APIRouter()

# Create an account
# POST Method
# /register

# authentication for users and set the session cookies
# POST Method
# /login

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
