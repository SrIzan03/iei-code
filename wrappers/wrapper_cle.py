# TODO: Implement
import pandas as pd
from lxml import etree

#tree = etree.parse("wrappers\data\monumentos.xml")

#nombres = tree.xpath("//monumentos/monumento/nombre/text()")

df = pd.read_xml("wrappers\data\monumentos.xml", xpath = ".//monumento")
    
for nombre, tipoMonumento, calle in zip(df['nombre'], df['tipoMonumento'], df['calle']):
    print(f"Nombre: {nombre}, tipoMonumento: {tipoMonumento}, calle: {calle}")