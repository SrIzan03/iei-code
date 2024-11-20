from dataclasses import dataclass
from enum import Enum

class Tipo(str, Enum):
    YACIMIENTO_ARQUELOGICO: 'yacimiento_arqueologico'
    IGLESIA_ERMITA: 'iglesia_ermita'
    MONASTERIO_CONVENTO = 'monasterio_convento'
    CASTILLO_FORTALEZA_TORRE = 'castillo_fortaleza_torre'
    EDIFICIO_SINGULAR = 'edificio_singular'
    PUENTE = 'puente'
    OTROS = 'otros'

@dataclass
class Provincia:
    codigo: int
    nombre: str

@dataclass
class Localidad:
    codigo: int
    nombre: str
    provincia_cod: int

@dataclass
class Monumento:
    codigo: int
    nombre: str
    tipo: Tipo
    direccion: str
    codigo_postal: str
    longitud: float
    latitud: float
    descripcion: str
    localidad_cod: int 
