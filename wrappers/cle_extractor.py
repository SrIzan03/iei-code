import pandas as pd
import xml.etree.ElementTree as ET

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
monumento_tipos = df_json['tipoMonumento']
monumento_direcciones = df_json['calle']
monumento_codigos_postales = df_json['codigoPostal']

monumento_longitudes = df_json['coordenadas'].apply(lambda x: x['longitud'])
monumento_latitudes = df_json['coordenadas'].apply(lambda x: x['latitud'])
# localidad_nombres = df_json['poblacion'].apply(lambda x: x['localidad'])
# poblacion_nombres = df_json['poblacion'].apply(lambda x: x['provincia'])

print(monumento_latitudes)

#for nombre, tipoMonumento, calle in zip(df_json['nombre'], df_json['tipoMonumento'], df_json['calle']):
 #   print(f"Nombre: {nombre}, tipoMonumento: {tipoMonumento}, calle: {calle}")
