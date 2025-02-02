from fastapi import FastAPI, HTTPException

def wrap():
    import os
    import subprocess
    import pandas as pd

    working_directory = os.getcwd()
    DATA_ROUTE = rf"{working_directory}/edificios_final.json"
    DATA_ROUTE_TEMP = rf"{working_directory}/edificios_final_temp.json"
    SCRIPT_ROUTE = rf"{working_directory}/utils/DeleteDuplicates.ps1"
    command = f'pwsh -File "{SCRIPT_ROUTE}" -InputFile "{DATA_ROUTE}" -OutputFile "{DATA_ROUTE_TEMP}"'

    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(result.stderr)

    df = pd.read_json(DATA_ROUTE_TEMP)
    return df.to_json()

app = FastAPI()
@app.get("/data", summary="Extraer información de fuente de datos", description="Extrae la información de la fuente de datos 'edificios_final.json'", tags=["Data"])
async def get_data():
    try:
        return wrap()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")