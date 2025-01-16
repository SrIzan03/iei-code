from fastapi import FastAPI

def wrap():
    import pandas as pd

    df = pd.read_csv('bienes_inmuebles_interes_cultural_entrega_final.csv', delimiter=";")
    return df.to_json()

app = FastAPI()
@app.get("/data")
async def get_data():
    return wrap()