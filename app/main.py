# main.py

# imports
from fastapi import FastAPI, Request
from app.api import endpoints

# application instance
app = FastAPI()

# Endpoint for basic message
@app.get("/")
async def root():
    return {"message": "Hello World"} 


