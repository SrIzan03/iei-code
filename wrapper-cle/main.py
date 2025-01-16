from fastapi import FastAPI

def wrap():
    import xml.etree.ElementTree as ET
    import pandas as pd

    tree = ET.parse("monumentos_entrega_final.xml")
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
    return json

app = FastAPI()
@app.get("/data")
async def get_data():
    return wrap()