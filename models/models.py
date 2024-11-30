from dataclasses import dataclass
from enum import Enum

class Tipo(str, Enum):
    YACIMIENTO_ARQUEOLOGICO = 'Yacimiento arqueologico' # type: ignore
    IGLESIA_ERMITA = 'Iglesia_Ermita' # type: ignore
    MONASTERIO_CONVENTO = 'Monasterio_Convento'
    CASTILLO_FORTALEZA_TORRE = 'Castillo-Fortaleza-Torre'
    EDIFICIO_SINGULAR = 'Edificio singular'
    PUENTE = 'Puente'
    OTROS = 'Otros'

@dataclass
class Provincia:
    codigo: int
    nombre: str

@dataclass
class ProvinciaCreate:
    nombre: str

@dataclass
class Localidad:
    codigo: int
    nombre: str
    provincia_cod: int

@dataclass
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

@dataclass
class MonumentoCreate:
    nombre: str
    tipo: Tipo
    direccion: str
    codigo_postal: str
    longitud: float
    latitud: float
    descripcion: str