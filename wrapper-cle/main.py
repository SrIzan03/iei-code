from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

def wrap():
    import xml.etree.ElementTree as ET
    import pandas as pd

    tree = ET.parse("monumentos_final.xml")
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
@app.get("/data", summary="Extraer información de fuente de datos", description="Extrae la información de la fuente de datos 'monumentos_final.xml'", tags=["Data"])
async def get_data():
    try:
        return wrap()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")