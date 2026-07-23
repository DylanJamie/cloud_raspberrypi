# file_helper.py

# functions needed for endpoints

# imports
import models

# register
# add a new user to the data base
# assign a user_id
# allow them to type an init username and pass
# later make them auto sign in or force them to the log in page
def usr_register():
    pass

# login
# Grab and varify the user credentials
# First check to see if the user exists
# decrypt their password
# check to see if password is correct
# if correct show file system or home screen
def usr_login():
    pass

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

