import numpy
import pandas as pd

from io import StringIO
from models import Tipo
from services import insert_into_db, get_eus_data

tipo_mapping = {
    "Zona arqueológica": Tipo.YACIMIENTO_ARQUEOLOGICO,
    "Yacimiento": Tipo.YACIMIENTO_ARQUEOLOGICO,

    "Iglesia": Tipo.IGLESIA_ERMITA,
    "Catedral": Tipo.IGLESIA_ERMITA,
    "Parroquia": Tipo.IGLESIA_ERMITA,
    "Basílica": Tipo.IGLESIA_ERMITA,
    "Ermita": Tipo.IGLESIA_ERMITA,

    "Santuario": Tipo.MONASTERIO_CONVENTO,
    "Monasterio": Tipo.MONASTERIO_CONVENTO,
    "Convento": Tipo.MONASTERIO_CONVENTO,

    "Fuerte": Tipo.CASTILLO_FORTALEZA_TORRE,
    "Castillo": Tipo.CASTILLO_FORTALEZA_TORRE,
    "Torre": Tipo.CASTILLO_FORTALEZA_TORRE,
    "Muralla": Tipo.CASTILLO_FORTALEZA_TORRE,

    "Villa": Tipo.EDIFICIO_SINGULAR,
    "Casa Consistorial": Tipo.EDIFICIO_SINGULAR,
    "Palacio": Tipo.EDIFICIO_SINGULAR,
    "Ayuntamiento": Tipo.EDIFICIO_SINGULAR,

    "Puente": Tipo.PUENTE,

    "otros": Tipo.OTROS
}

def determinar_tipo(nombre, tipo_mapping):
    for palabra_clave, tipo in tipo_mapping.items():
        if palabra_clave.lower() in nombre.lower():
            return tipo
    return Tipo.OTROS

def check_direccion(direccion: str):
    if direccion is numpy.nan: 
        # Llamar al servicio que tiene la API para obtener la dirección a través de las coordenadas.
        return "dirección vacía"
    else:
        return direccion

def extract(json: str):
    df = pd.read_json(StringIO(json))

    monumento_nombres = df["documentName"]
    monumento_tipos = df["documentName"].apply(lambda x: determinar_tipo(x, tipo_mapping))
    monumento_direcciones = df["address"].fillna("")
    monumento_codigos_postales = df["postalCode"].fillna("")
    monumento_longitudes = df["lonwgs84"]
    monumento_latitudes = df["latwgs84"]
    monumento_descripciones = df["documentDescription"]

    localidad_nombres = df["municipality"].fillna("")

    provincia_nombres = df["territory"]
    from models import MonumentoCreate, LocalidadCreate, ProvinciaCreate
    for i in range(len(monumento_nombres)):
        monumento = MonumentoCreate(
            monumento_nombres[i],
            monumento_tipos[i],
            monumento_direcciones[i],
            monumento_codigos_postales[i],
            monumento_longitudes[i],
            monumento_latitudes[i],
            monumento_descripciones[i],
        )
        localidad = LocalidadCreate(
            localidad_nombres[i],
        )
        provincia = ProvinciaCreate(
            provincia_nombres[i],
        )
        insert_into_db('eus', monumento, localidad, provincia)

def extract_eus():
    data = get_eus_data()
    extract(data)