from models import MonumentoCreate, LocalidadCreate, ProvinciaCreate, Provincia, Monumento, Localidad
from data import get_provincia_by_nombre, get_localidad_by_nombre, get_monumento_by_nombre, create_provincia, create_localidad, create_monumento 
from .geo_api_service import get_direccion_and_cod_postal 
from utils import MyLogger

logger = MyLogger()

def insert_into_db(dataSource: str, monumento: MonumentoCreate, localidad: LocalidadCreate, provincia: ProvinciaCreate):
    if not monumento.latitud or not monumento.longitud:
        logger.log_excluded(dataSource, monumento.nombre, localidad.nombre, 'Error in coordinates: Empty latitud or longitud')
        return
    
    if not float_format(monumento.latitud) or not float_format(monumento.longitud):
        logger.log_excluded(dataSource, monumento.nombre, localidad.nombre, 'Error in coordinates: Wrong float format')
        return

    if not lat_long_range_value(monumento.latitud, monumento.longitud):
        logger.log_excluded(dataSource, monumento.nombre, localidad.nombre, 'Error in coordinates: Out of range')
        return

    provincia_model = create_provincia_model(provincia)
    localidad_model = create_localidad_model(localidad, provincia_model)
    create_monumento_model(dataSource, monumento, localidad_model)

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

def exists_monumento(mon_nombre: str):
    existing_monumento = get_monumento_by_nombre(mon_nombre)
    if existing_monumento:
        return existing_monumento
    
def lat_long_range_value(lat, long):
    try:
        lat_int = int(str(lat).split('.')[0])
        long_int = int(str(long).split('.')[0])

        return lat_int >= -90 and lat_int <= 90 and long_int >= -180 and long_int <= 180
    except ValueError:
        return False

def float_format(value):
    value_str = str(value)
    value_str = value_str.replace('-', '', 1)

    if value_str.replace('.', '', 1).isdigit():
        return True
    else:
        return False

def create_monumento_model(dataSource: str, monumento: MonumentoCreate, localidad: Localidad):
    existing_monumento = get_monumento_by_nombre(monumento.nombre)
    if existing_monumento:
        logger.log_excluded(dataSource, monumento.nombre, localidad.nombre, 'Error in monument: Already exists')
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
        logger.log_succeded(monumento.nombre)
        return m