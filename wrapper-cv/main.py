from fastapi import FastAPI, HTTPException

def wrap():
    import pandas as pd

    df = pd.read_csv('bienes_inmuebles_interes_cultural_final.csv', delimiter=";")
    return df.to_json()

app = FastAPI()
@app.get("/data", summary="Extraer información de fuente de datos", description="Extrae la información de la fuente de datos 'bienes_inmuebles_interes_cultural_final.csv'", tags=["Data"])
async def get_data():
    try:
        return wrap()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")