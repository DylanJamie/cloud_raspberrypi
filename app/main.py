# main.py

# imports
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
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
    return RedirectResponse(url="/login")

# Get the login HTML file
@app.get("/login")
async def login_html_page():
    return FileResponse("app/templates/login.html")

# Get the dashboard HTML file
@app.get("/dashboard")
async def dashboard_html_page():
    return FileResponse("app/templates/dashboard.html")

# Get the dashboard when you click on the forget pass word button
@app.get("/forgot_pass")
async def forgot_pass_html_page():
    return FileResponse("app/templates/forgot_pass.html")

# Get the dashboard when you click on the Create Account button
@app.get("/create_account")
async def create_account_html_page():
    return FileResponse("app/templates/create_account.html")

