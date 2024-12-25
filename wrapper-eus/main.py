from fastapi import FastAPI

def wrap():
    import os
    import subprocess
    import pandas as pd

    working_directory = os.getcwd()
    DATA_ROUTE = rf"{working_directory}/edificios_entrega1.json"
    DATA_ROUTE_TEMP = rf"{working_directory}/edificios_entrega1_temp.json"
    SCRIPT_ROUTE = rf"{working_directory}/utils/DeleteDuplicates.ps1"
    command = f'pwsh -File "{SCRIPT_ROUTE}" -InputFile "{DATA_ROUTE}" -OutputFile "{DATA_ROUTE_TEMP}"'

    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(result.stderr)

    df = pd.read_json(DATA_ROUTE_TEMP)
    return df.to_json()

app = FastAPI()
@app.get("/data")
async def get_data():
    return wrap()