from typing import Final

import requests

CLE_URL: Final[str]= "http://wrapper-cle:8001"
CV_URL: Final[str]= "http://wrapper-cv:8002"
EUS_URL: Final[str]= "http://wrapper-eus:8003"
DATA_ENDPOINT: Final[str]= "/data"

def get_cle_data():
    response = requests.get(CLE_URL + DATA_ENDPOINT)
    return response.json()

def get_cv_data():
    response = requests.get(CV_URL + DATA_ENDPOINT)
    return response.json()

def get_eus_data():
    response = requests.get(EUS_URL + DATA_ENDPOINT)
    return response.json()