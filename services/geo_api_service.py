import requests
from string import Template

def get_direccion_and_cod_postal(lat: str, lon: str):
    t = Template('https://nominatim.openstreetmap.org/reverse?format=json&lat=$lat&lon=$lon')
    
    headers = {"User-Agent": "IEI_04/1.0"}
    r = requests.get(
            t.substitute(lat=lat, lon=lon),
            headers=headers
        )
    
    json = r.json()
    address_json = json['address']

    cod = get_post_cod(address_json)
    dir = get_dir(address_json)

    return dir, cod

def get_post_cod(address_json):
    return address_json['postcode']

def get_dir(address_json):
    localidad_keys = ['road', 'amenity']
    
    for key in localidad_keys:
        localidad = address_json.get(key)
        if localidad:
            return localidad
        
    return ""