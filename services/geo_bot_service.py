from string import Template
import requests
import os

def utm_to_lat_long(utm_north: str, utm_east:str):
    url = "http://localhost:8000"
    t = Template("/utm-to-lat-long/$north/$east")

    bot_url = url + t.substitute(north= utm_north, east= utm_east)
    response = requests.get(bot_url)
    return response.json()