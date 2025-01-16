import database as database
import utils.remove_logs
from extractors import extract_cv, extract_cle, extract_eus
from dotenv import load_dotenv
from database import create_database, clean_database
from data import get_all_monuments

from utils import logger
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models import Tipo

app = FastAPI()

logger = logger.MyLogger()

load_dotenv()

# More detailed CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

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

@app.get("/logs")
async def get_logs():
    succeded = logger.succeded_counter
    repaired_content = logger.get_logs('repaired')
    excluded_content = logger.get_logs('excluded')
    result = "Número de registros cargados correctamente: " + str(succeded) + "\n\n" + "Registros con errores y reparados:\n" + repaired_content + "\n\n" + "Registros con errores y rechazados: \n" + excluded_content
    return JSONResponse(content=result)

@app.get("/monuments")
async def get_monuments():
    monuments = get_all_monuments()
    transformed_monuments = [
        {
            "nombre": monument[0],
            "tipo": monument[1],
            "direccion": monument[2],
            "codigo_postal": monument[3],
            "longitud": monument[4],
            "latitud": monument[5],
            "descripcion": monument[6],
            "localidad_cod": monument[7]
        }
        for monument in monuments
    ]
    return JSONResponse(content={"monuments": transformed_monuments})

@app.get("/types")
async def get_types():
    types = [tipo.value for tipo in Tipo]
    return JSONResponse(content={"types": types})
