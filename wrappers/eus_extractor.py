import os
import subprocess
import pandas as pd
from models import Tipo
import numpy
from services import insert_into_db

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
    

# Wrapper : In the future the wrapper will return all the json data to the extractor instead of the extractor reading it directly.
working_directory = os.getcwd()
DATA_ROUTE = rf"{working_directory}\wrappers\data_sources\edificios_entrega1.json"
DATA_ROUTE_TEMP = rf"{working_directory}\wrappers\data_sources\edificios_entrega1_temp.json"
SCRIPT_ROUTE = rf"{working_directory}\utils\DeleteDuplicates.ps1"
command = f'powershell -File "{SCRIPT_ROUTE}" -InputFile "{DATA_ROUTE}" -OutputFile "{DATA_ROUTE_TEMP}"'

result = subprocess.run(command, shell=True, capture_output=True, text=True)

# Extractor: Read json data from the wrapper and filters the corresponding data to add them to the DB.

df = pd.read_json(DATA_ROUTE_TEMP)

monumento_nombres = df["documentName"]
monumento_tipos = df["documentName"].apply(lambda x: determinar_tipo(x, tipo_mapping))
monumento_direcciones = df["address"].fillna("")
monumento_codigos_postales = df["postalCode"].fillna("")
monumento_longitudes = df["lonwgs84"]
monumento_latitudes = df["latwgs84"]
monumento_descripciones = df["documentDescription"]

localidad_nombres = df["municipality"].fillna("")

provincia_nombres = df["territory"]

def extract_eus():
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
        insert_into_db(monumento, localidad, provincia)



def print_codigo():
    with open('resultados.txt', 'w', encoding='UTF-8') as file:
        for i in range(provincia_nombres.size):
            file.write(str(provincia_nombres[i]) + '\n')

    print(monumento_direcciones[38])