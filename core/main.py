import database as database
import utils.remove_logs
from extractors import extract_cv, extract_cle, extract_eus
from dotenv import load_dotenv
from database import create_database, clean_database

from utils import logger
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

logger = logger.MyLogger()

load_dotenv()

@app.get("/load/cv")
async def load_cv():
    extract_cv()
    return logger.get_counts()

@app.get("/load/cle")
async def load_cle():
    extract_cle()
    return logger.get_counts()

@app.get("/load/eus")
async def load_eus():
    extract_eus()
    return logger.get_counts()

@app.get("/database/create_tables")
async def database_create():
    create_database()
    return JSONResponse(content={"message": "Database created"})

@app.get("/database/remove_tables")
async def database_clean():
    clean_database()
    return JSONResponse(content={"message": "Database cleaned"})

@app.get("/database/init")
async def database_init():
    clean_database()
    create_database()
    return JSONResponse(content={"message": "Database initialized"})