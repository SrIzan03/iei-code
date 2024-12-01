from models import MonumentoCreate, LocalidadCreate, ProvinciaCreate, Provincia, Monumento, Localidad
from data import get_provincia_by_nombre, get_localidad_by_nombre, get_monumento_by_nombre, create_provincia, create_localidad, create_monumento 
from .geo_api_service import get_direccion_and_cod_postal 

def insert_into_db(monumento: MonumentoCreate, localidad: LocalidadCreate, provincia: ProvinciaCreate):
    if not monumento.latitud or not monumento.longitud:
        return
    provincia_model = create_provincia_model(provincia)
    localidad_model = create_localidad_model(localidad, provincia_model)
    create_monumento_model(monumento, localidad_model)

def create_provincia_model(provincia: ProvinciaCreate):
    existing_provincia = get_provincia_by_nombre(provincia.nombre.upper())
    if existing_provincia:
        return existing_provincia
    else:
        p = Provincia(None, provincia.nombre.upper())
        create_provincia(p)
        return p

def create_localidad_model(localidad: LocalidadCreate, provincia: Provincia):
    existing_localidad = get_localidad_by_nombre(localidad.nombre.upper())
    if existing_localidad:
        return existing_localidad
    else:
        l = Localidad(None, localidad.nombre.upper(), provincia.codigo)
        create_localidad(l)
        return l

skip_count = 0

def create_monumento_model(monumento: MonumentoCreate, localidad: Localidad):
    global skip_count
    existing_monumento = get_monumento_by_nombre(monumento.nombre)
    if existing_monumento:
        skip_count += 1
        print(f"Monumento {monumento.nombre} already exists. Skipped {skip_count} times.")
        return existing_monumento
    else:
        codigo_postal = monumento.codigo_postal
        direccion = monumento.direccion

        if codigo_postal == '' and direccion == '':
            direccion, codigo_postal = get_direccion_and_cod_postal(monumento.latitud, monumento.longitud)
        elif direccion == '':
            direccion, _ = get_direccion_and_cod_postal(monumento.latitud, monumento.longitud)
        elif codigo_postal == '': 
            _, codigo_postal = get_direccion_and_cod_postal(monumento.latitud, monumento.longitud)

        if codigo_postal != '':
            codigo_postal = f"{int(codigo_postal):05}"

        m = Monumento(
            monumento.nombre,
            monumento.tipo,
            direccion,
            codigo_postal,
            monumento.longitud,
            monumento.latitud,
            monumento.descripcion,
            localidad.codigo
        )
        create_monumento(m)
        return m

def exists_monumento(mon_nombre: str):
    existing_monumento = get_monumento_by_nombre(mon_nombre)
    if existing_monumento:
        return existing_monumento