import pandas as pd
from models import Tipo, MonumentoCreate, ProvinciaCreate, LocalidadCreate
from services import get_direccion_and_cod_postal, utm_to_lat_long

def wrap() -> str:
    df = pd.read_csv('./wrappers/data_sources/bienes_inmuebles_interes_cultural.csv', delimiter=";")
    return df.to_json()

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

# TODO: refactor, in the future we will not pass a str
def extract(json: str):
    df = pd.read_json(json)

    for _, row in df.iterrows():
        response = utm_to_lat_long(row['UTMNORTE'],row['UTMESTE'])
        denominacion = row['DENOMINACION']
        codCategoria = row['CODCATEGORIA']

        tipo = getTipo(denominacion, codCategoria)
        latitude = response.get('latitude')
        longitude = response.get('longitude')
        direccion, postCode = get_direccion_and_cod_postal(latitude, longitude)

        monumento = MonumentoCreate(
            denominacion,
            tipo,
            direccion,
            postCode,
            longitude,
            latitude,
            ''
        )

        localidad = LocalidadCreate(row['MUNICIPIO'])

        provincia = ProvinciaCreate(row['PROVINCIA'])