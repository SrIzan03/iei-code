import database as database
from extractors import extract_cv, extract_cle, extract_eus
from dotenv import load_dotenv
from database import create_database, clean_database
from data import get_all_monuments, get_filtered_monuments
from fastapi import Query


from utils import logger
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models import Tipo

app = FastAPI()

logger = logger.MyLogger()

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,)

@app.get("/load/cv", summary="Cargar datos de la Comunidad Valenciana", description="Carga los datos de la Comunidad Valenciana haciendo uso de un wrapper y un extractor.", tags=["Loader"])
async def load_cv():
    try:
        extract_cv()
        return JSONResponse(status_code=200, content={"message": "Datos cargados correctamente"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")

@app.get("/load/cle", summary="Cargar datos de Castilla y León", description="Carga los datos de Castilla y León haciendo uso de un wrapper y un extractor.", tags=["Loader"])
async def load_cle():
        extract_cle()
        return JSONResponse(status_code=200, content={"message": "Datos cargados correctamente"})

@app.get("/load/eus", summary="Cargar datos de Euskadi", description="Carga los datos de Euskadi haciendo uso de un wrapper y un extractor.", tags=["Loader"])
async def load_eus():
    try:
        extract_eus()
        return JSONResponse(status_code=200, content={"message": "Datos cargados correctamente"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")

@app.get("/database/create_tables", summary="Crear tablas de BD", description="Crea las tablas de Base de Datos necesarias para la posterior extracción.", tags=["Database"])
async def database_create():
    try:
        create_database()
        return JSONResponse(status_code=201, content={"message": "Tablas de Base de Datos creadas con éxito"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")

@app.get("/database/remove_tables", summary="Elimina las tablas de BD", description="Elimina las tablas de Base de Datos con el fin de limpiar los datos en ella.", tags=["Database"])
async def database_clean():
    try:
        clean_database()
        return JSONResponse(status_code=200, content={"message": "Tablas de Base de Datos eliminadas con éxito"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")

@app.get("/database/init", summary="Inicializa la BD", description="Inicializa la Base de Datos limpiando sus tablas y datos, y volviéndola a crear.", tags=["Database"])
async def database_init():
    try:
        clean_database()
        create_database()
        return JSONResponse(status_code=200, content={"message": "Base de datos inicializada con éxito"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")

@app.get("/logs", summary="Consume los registros", description="Consume los registros generados por las operaciones de carga", tags=["Logs"])
async def get_logs():
    try:
        succeded = logger.succeded_counter
        repaired_content = logger.get_logs('repaired')
        excluded_content = logger.get_logs('excluded')
        result = "Número de registros cargados correctamente: " + str(succeded) + "\n\n" + "Registros con errores y reparados:\n" + repaired_content + "\n\n" + "Registros con errores y rechazados: \n" + excluded_content
        logger.reset_logs()
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")

@app.get("/monuments", summary="Obtiene todos los monumentos que coincidan con los filtros", description="Obtiene todos los monumentos registrados en Base de Datos que coincidan con los filtros proporcionados", tags=["Search"])
async def get_monuments(
    localidad: str = Query(None, description="Filter by localidad name"),
    codigo_postal: str = Query(None, description="Filter by postal code"),
    provincia: str = Query(None, description="Filter by provincia name"),
    tipo: Tipo = Query(None, description="Filter by monument type")
):
    monuments = get_filtered_monuments(localidad, codigo_postal, provincia, tipo)
    transformed_monuments = [
        {
            "nombre": monument[0],
            "tipo": monument[1],
            "direccion": monument[2],
            "codigo_postal": monument[3],
            "longitud": monument[4],
            "latitud": monument[5],
            "descripcion": monument[6],
            "localidad": monument[7],
            "provincia": monument[8]
        }
        for monument in monuments
    ]
    return JSONResponse(content={"monuments": transformed_monuments})

@app.get("/types", summary="Obtiene todos los tipos de monumentos", description="Obtiene todos los tipos de monumentos registrados en Base de Datos", tags=["Search"])
async def get_types():
    types = [tipo.value for tipo in Tipo]
    return JSONResponse(content={"types": types})

database_init()