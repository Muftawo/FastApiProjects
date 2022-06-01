from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.openapi.utils import get_openapi


app = FastAPI()

@app.get("/")
def write_home():
    return {
        "tutorail": "Hello World",
        "page": "home",
    }


@app.get("/about")
def write_about():
    return {
        "tutorail": "Hello World",
        "page": "about",
    }

@app.pos