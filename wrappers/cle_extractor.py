# TODO: Implement
import pandas as pd
from lxml import etree


#wrapper
df = pd.read_xml("wrappers\data\monumentos.xml", xpath = ".//monumento")
json = df.to_json(orient="records", indent=4)

#extractor
df_json = pd.read_json(json)

print(df_json['calle'])

#for nombre, tipoMonumento, calle in zip(df_json['nombre'], df_json['tipoMonumento'], df_json['calle']):
 #   print(f"Nombre: {nombre}, tipoMonumento: {tipoMonumento}, calle: {calle}")
