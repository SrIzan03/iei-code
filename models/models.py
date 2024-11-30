from dataclasses import dataclass
from enum import Enum

class Tipo(str, Enum):
    YACIMIENTO_ARQUEOLOGICO = 'yacimiento_arqueologico' # type: ignore
    IGLESIA_ERMITA = 'iglesia_ermita' # type: ignore
    MONASTERIO_CONVENTO = 'monasterio_convento'
    CASTILLO_FORTALEZA_TORRE = 'castillo_fortaleza_torre'
    EDIFICIO_SINGULAR = 'edificio_singular'
    PUENTE = 'puente'
    OTROS = 'otros'

@dataclass
class Provincia:
    codigo: int
    nombre: str

class ProvinciaCreate:
    nombre: str

@dataclass
class Localidad:
    codigo: int
    nombre: str
    provincia_cod: int

class LocalidadCreate:
    nombre: str

@dataclass
class Monumento:
    nombre: str
    tipo: Tipo
    direccion: str
    codigo_postal: str
    longitud: float
    latitud: float
    descripcion: str
    localidad_cod: int 

class MonumentoCreate:
    nombre: str
    tipo: Tipo
    direccion: str
    codigo_postal: str
    longitud: float
    latitud: float
    descripcion: str