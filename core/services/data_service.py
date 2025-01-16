from models import MonumentoCreate, LocalidadCreate, ProvinciaCreate, Provincia, Monumento, Localidad
from data import get_provincia_by_nombre, get_localidad_by_nombre, get_monumento_by_nombre, create_provincia, create_localidad, create_monumento 
from .geo_api_service import get_direccion_and_cod_postal 
from utils import MyLogger

logger = MyLogger()

provincias_nombres = ["GIPUZKOA", "BIZKAIA", "ARABA/ÁLAVA", "ÁVILA", "VALLADOLID", "BURGOS", "SEGOVIA", "SALAMANCA", "LEÓN", "ZAMORA", "SORIA", "PALENCIA", "VALENCIA", "ALICANTE", "CASTELLÓN"]

cp_mapping = {
    "01": "ARABA/ÁLAVA",
    "20": "GIPUZKOA",
    "48": "BIZKAIA",

    "05": "ÁVILA",
    "47": "VALLADOLID",
    "09": "BURGOS",
    "40": "SEGOVIA",
    "37": "SALAMANCA",
    "24": "LEÓN",
    "49": "ZAMORA",
    "42": "SORIA",
    "34": "PALENCIA",

    "46": "VALENCIA",
    "03": "ALICANTE",
    "12": "CASTELLÓN",
}

def determinar_provincia(code, cp_mapping):
    for cp, provincia in cp_mapping.items():
        if (code == cp) :
            return provincia

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

    provincia_model = create_provincia_model(provincia, monumento)
    localidad_model = create_localidad_model(localidad, provincia_model)
    create_monumento_model(dataSource, monumento, localidad_model)

def create_provincia_model(provincia: ProvinciaCreate, monumento: MonumentoCreate):
    existing_provincia = get_provincia_by_nombre(provincia.nombre.upper())
    if existing_provincia:
        return existing_provincia
    else:
        if(check_provincia_name(provincia.nombre.upper())):
            p = Provincia(None, provincia.nombre.upper())
            create_provincia(p)
            return p
        else:
            _, codigo_postal = get_direccion_and_cod_postal(monumento.latitud, monumento.longitud)
            provincia_name = determinar_provincia(codigo_postal, cp_mapping)
            existing_provincia = get_provincia_by_nombre(provincia.nombre.upper())
            if existing_provincia:
                return existing_provincia
            
            p = Provincia(None, provincia_name.nombre.upper())
            create_provincia(p)

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
    
def check_provincia_name(name):
    if (name in provincias_nombres):
        return True
    else:
        return False

def float_format(value):
    value_str = str(value)
    value_str = value_str.replace('-', '', 1)

    if value_str.replace('.', '', 1).isdigit():
        return True
    else:
        return False
    
def postal_code_length(postal_code, dataSource, monumento, localidad):
    postal_code_str = float_to_str(postal_code)
    if len(postal_code_str) <= 3 or len(postal_code_str) > 5:
        logger.log_excluded(dataSource, monumento.nombre, localidad.nombre, 'Error in postal code: Wrong postal code length')
        return False
    elif len(postal_code_str) == 4:
        logger.log_repaired(dataSource, monumento.nombre, localidad.nombre, 'Error in postal code: postal code length is 4', "A 0 has been added to the postal code")
        return True
    else:
        return True

def float_to_str(value):
    try:
        # Attempt to convert to a float
        value = float(value)
        # Check if it's an integer-like float
        return str(int(value)) if value.is_integer() else str(value)
    except ValueError:
        # If conversion fails, assume it's a string and return as-is
        return str(value)
    
def postal_code_range_value(value):
    postal_code_identifier = int(value[:2])

    if 1 <= postal_code_identifier <= 52:
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

        if codigo_postal == '':
            logger.log_excluded(dataSource, monumento.nombre, localidad.nombre, 'Error in postal code: Wrong postal code format')
            return
        
        if postal_code_length(codigo_postal, dataSource, monumento, localidad):
            codigo_postal = f"{int(codigo_postal):05}"
        else:
            return

        if not postal_code_range_value(codigo_postal):
            logger.log_excluded(dataSource, monumento.nombre, localidad.nombre, 'Error in postal code: The postal code does not exist in Spain')
            return

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