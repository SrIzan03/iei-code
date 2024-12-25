import pandas as pd
import re

from io import StringIO
from models import Tipo
from services import insert_into_db, get_cle_data

# Define a mapping that converts the monumento_tipos to the Tipo enum
tipo_mapping = {
    'Yacimientos arqueológicos': Tipo.YACIMIENTO_ARQUEOLOGICO,

    'Iglesias y Ermitas': Tipo.IGLESIA_ERMITA,
    'Santuarios': Tipo.IGLESIA_ERMITA,
    'Catedrales': Tipo.IGLESIA_ERMITA,

    'Monasterios': Tipo.MONASTERIO_CONVENTO,

    'Castillos': Tipo.CASTILLO_FORTALEZA_TORRE,
    'Torres': Tipo.CASTILLO_FORTALEZA_TORRE,
    'Murallas y puertas': Tipo.CASTILLO_FORTALEZA_TORRE,

    'Casas Consistoriales': Tipo.EDIFICIO_SINGULAR,
    'Casas nobles': Tipo.EDIFICIO_SINGULAR,
    'Palacios': Tipo.EDIFICIO_SINGULAR,
    'Reales Sitios': Tipo.EDIFICIO_SINGULAR,
    'Sinagogas': Tipo.EDIFICIO_SINGULAR,
    'Otros edificios': Tipo.EDIFICIO_SINGULAR,

    'Puentes': Tipo.PUENTE,

    'otros': Tipo.OTROS
}

char_mapping = {
    '&oacute;': 'ó',
    '&aacute;': 'á',
    '&eacute;': 'é',
    '&iacute;': 'í',
    '&uacute;': 'ú',
    '&ntilde;': 'ñ',
}

def replace_html_entities(text):
    if text is None:
        return ''
    for entity, char in char_mapping.items():
        text = text.replace(entity, char)
    return text

def clean_html_tags(text):
    if text is None:
        return ''
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def extract(json: str):
    df_json = pd.read_json(StringIO(json))

    monumento_nombres = df_json['nombre']
    monumento_tipos = df_json['tipoMonumento'].apply(lambda x: tipo_mapping.get(x, Tipo.OTROS))
    monumento_direcciones = df_json['calle'].fillna('')
    monumento_codigos_postales = df_json['codigoPostal'].fillna('')
    monumento_descripciones = df_json['Descripcion'].apply(replace_html_entities)
    monumento_descripciones = monumento_descripciones.apply(clean_html_tags)

    monumento_longitudes = df_json['coordenadas'].apply(lambda x: x['longitud'])
    monumento_latitudes = df_json['coordenadas'].apply(lambda x: x['latitud'])
    localidad_nombres = df_json['poblacion'].apply(lambda x: x['localidad'] if x is not None else '')
    provincia_nombres = df_json['poblacion'].apply(lambda x: x['provincia'] if x is not None else '')

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
        insert_into_db('cle', monumento, localidad, provincia)

def extract_cle():
    data = get_cle_data()
    extract(data)