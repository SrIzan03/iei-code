import pandas as pd

from io import StringIO
from math import isnan
from models import Tipo, MonumentoCreate, ProvinciaCreate, LocalidadCreate
from services import utm_to_lat_long, insert_into_db, exists_monumento, get_cv_data, get_direccion_and_cod_postal

def getTipo(denominacion: str, codCategoria: int):
    denominacion = denominacion.lower()

    if codCategoria in [5, 7]:
        return Tipo.YACIMIENTO_ARQUEOLOGICO
    if any(keyword in denominacion for keyword in ["iglesia", "ermita"]):
        return Tipo.IGLESIA_ERMITA
    if any(keyword in denominacion for keyword in ["monasterio", "convento"]):
        return Tipo.MONASTERIO_CONVENTO
    if any(keyword in denominacion for keyword in ["castillo", "fortaleza", "torre"]):
        return Tipo.CASTILLO_FORTALEZA_TORRE
    if codCategoria in [11]:
        return Tipo.EDIFICIO_SINGULAR
    if "puente" in denominacion:
        return Tipo.PUENTE
    return Tipo.OTROS

def extract(json: str):
    df = pd.read_json(StringIO(json))

    for _, row in df.iterrows():
        denominacion = row['DENOMINACION']
        if exists_monumento(denominacion):
            continue

        utm_norte = row['UTMNORTE']
        utm_este = row['UTMESTE']
        if isnan(utm_este) or isnan(utm_norte):
            continue

        response = utm_to_lat_long(utm_norte, utm_este)

        codCategoria = row['CODCATEGORIA']

        tipo = getTipo(denominacion, codCategoria)
        latitude = response.get('latitude')
        longitude = response.get('longitude')

        if longitude and latitude:
            dir, cp = get_direccion_and_cod_postal(latitude, longitude)

        monumento = MonumentoCreate(
            denominacion,
            tipo,
            dir,
            cp,
            longitude,
            latitude,
            ''
        )

        localidad = LocalidadCreate(row['MUNICIPIO'])

        provincia = ProvinciaCreate(row['PROVINCIA'])

        insert_into_db('cv', monumento, localidad, provincia)

def extract_cv():
    data = get_cv_data()
    extract(data)