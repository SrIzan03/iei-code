import pandas as pd
import requests
from models.models import Tipo

def wrap() -> str:
    df = pd.read_csv('./wrappers/data_sources/bienes_inmuebles_interes_cultural.csv', delimiter=";")
    return df.to_json()

def getTipo(denominacion: str, codCategoria: int):
    if codCategoria in [5, 7]:
        return Tipo.YACIMIENTO_ARQUELOGICO
    if denominacion in ["Iglesia", "Ermita"]:
        return Tipo.IGLESIA_ERMITA
    if denominacion in ["Monasterio", "Convento"]:
        return Tipo.MONASTERIO_CONVENTO
    if denominacion in ["Castillo", "Fortaleza", "Torre"]:
        return Tipo.CASTILLO_FORTALEZA_TORRE
    if codCategoria in [11]:
        return Tipo.EDIFICIO_SINGULAR
    if denominacion in ["Puente"]:
        return Tipo.PUENTE
    return Tipo.OTROS

# TODO: refactor, in the future we will not pass a str
def extract(json: str):
    df = pd.read_json(json)
    # CV['IGPCV', 'DENOMINACION', 'PROVINCIA', 'MUNICIPIO', 'UTMESTE', 'UTMNORTE', 'CODCLASIFICACION', 'CLASIFICACION', 'CODCATEGORIA', 'CATEGORIA']
    for tuple in df.itertuples():
        response = utm_to_lat_long(tuple['UTMNORTE'],tuple['UTMESTE'])
        denominacion = tuple['DENOMINACION']
        codCategoria = tuple['CODCATEGORIA']

        nombre = denominacion
        tipo = getTipo(denominacion, codCategoria)
        latitude = response.get('latitude')
        longitude = response.get('longitude')
        

def utm_to_lat_long(utm_north: str, utm_east:str):
    BOT_URL = "http://iei-bot:8000/utm-to-lat-long/utm_north/utm_east"
    response = requests.get(BOT_URL, params={"utm_north": utm_north, "utm_east": utm_east})
    return response.json()




json = wrap()
extract(json)