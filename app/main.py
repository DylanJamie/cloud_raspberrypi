# main.py

# imports
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api import endpoints
from app.database.database import init_db

# application instance
app = FastAPI()

# Pull everything together
@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(endpoints.router)

# Makes anything in app/static/ reachable at /static/...
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Endpoint for basic message
@app.get("/")
async def root():
    return FileResponse("app/templates/index.html") 


