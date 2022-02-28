from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from service import app


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
