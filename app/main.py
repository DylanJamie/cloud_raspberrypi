# main.py

# imports
from fastapi import FastAPI, Request
from app.api import endpoints
from app.database.database import init_db

# application instance
app = FastAPI()

# Pull everything together
@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(endpoints.router)
    
# Endpoint for basic message
@app.get("/")
async def root():
    return {"message": "Hello World"} 


