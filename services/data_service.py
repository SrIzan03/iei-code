from models import MonumentoCreate, LocalidadCreate, ProvinciaCreate, Provincia, Monumento, Localidad
from data import get_provincia_by_nombre, get_localidad_by_nombre, get_monumento_by_nombre, create_provincia, create_localidad, create_monumento 

def insert_into_db(monumento: MonumentoCreate, localidad: LocalidadCreate, provincia: ProvinciaCreate):
    provincia_model = create_provincia_model(provincia)
    localidad_model = create_localidad_model(localidad, provincia_model)
    print(localidad_model)
    monumento_model = create_monumento_model(monumento, localidad_model)
    create_monumento(monumento_model)

def create_provincia_model(provincia: ProvinciaCreate):
    existing_provincia = get_provincia_by_nombre(provincia.nombre)
    if existing_provincia:
        return existing_provincia.id
    else:
        p = Provincia(None, provincia.nombre)
        create_provincia(p)
        return p

def create_localidad_model(localidad: LocalidadCreate, provincia: Provincia):
    existing_localidad = get_localidad_by_nombre(localidad.nombre)
    if existing_localidad:
        return existing_localidad
    else:
        l = Localidad(None, localidad.nombre, provincia.codigo)
        create_localidad(l)
        return l

def create_monumento_model(monumento: MonumentoCreate, localidad: Localidad):
    existing_monumento = get_monumento_by_nombre(monumento.nombre)
    if existing_monumento:
        return existing_monumento
    else:
        return Monumento(
            monumento.nombre,
            monumento.tipo,
            monumento.direccion,
            monumento.codigo_postal,
            monumento.longitud,
            monumento.latitud,
            monumento.descripcion,
            localidad.codigo
        )