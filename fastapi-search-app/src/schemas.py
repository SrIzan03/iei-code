from pydantic import BaseModel
from typing import Optional

class MonumentoBase(BaseModel):
    nombre: str
    tipo: Optional[str] = None
    direccion: Optional[str] = None
    codigo_postal: Optional[str] = None
    longitud: Optional[str] = None
    latitud: Optional[str] = None
    descripcion: Optional[str] = None
    localidad_codigo: Optional[int] = None

class MonumentoCreate(MonumentoBase):
    pass

class MonumentoResponse(MonumentoBase):
    pass

class MonumentoSearch(MonumentoBase):
    pass