import pandas as pd
import xml.etree.ElementTree as ET

from models import Tipo

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

# Wrapper: Read XML and convert to JSON
tree = ET.parse("wrappers/data_sources/monumentos.xml")
root = tree.getroot()

data = []
for monumento in root.findall(".//monumento"):
    item = {}
    for child in monumento:
        if child.tag == 'coordenadas' or child.tag == 'poblacion':
            item[child.tag] = {subchild.tag: subchild.text for subchild in child}
        else:
            item[child.tag] = child.text
    data.append(item)

df = pd.DataFrame(data)
json = df.to_json(orient="records", indent=4)

# Extractor: Read JSON
df_json = pd.read_json(json)

monumento_nombres = df_json['nombre']
monumento_tipos = df_json['tipoMonumento'].apply(lambda x: tipo_mapping.get(x, Tipo.OTROS))
monumento_direcciones = df_json['calle']
monumento_codigos_postales = df_json['codigoPostal']
monumento_descripciones = df_json['Descripcion']

monumento_longitudes = df_json['coordenadas'].apply(lambda x: x['longitud'])
monumento_latitudes = df_json['coordenadas'].apply(lambda x: x['latitud'])
localidad_nombres = df_json['poblacion'].apply(lambda x: x['localidad'] if x is not None else '')
provincia_nombres = df_json['poblacion'].apply(lambda x: x['provincia'] if x is not None else '')
# poblacion_nombres = df_json['poblacion'].apply(lambda x: x['provincia'])

def pass_data_to_service():
    from models import MonumentoCreate, LocalidadCreate, ProvinciaCreate
    for i in range(len(monumento_nombres)):
        MonumentoCreate(
            monumento_nombres[i],
            monumento_tipos[i],
            monumento_direcciones[i],
            monumento_codigos_postales[i],
            monumento_longitudes[i],
            monumento_latitudes[i],
            '',
        )
        LocalidadCreate(
            localidad_nombres[i],
        )
        ProvinciaCreate(
            provincia_nombres[i],
        )

def print_example():
    print(monumento_descripciones)

def get_tipo():
    return tipo_mapping.get('Puentes', Tipo.OTROS)