from typing import List, Optional

class Monumento:
    def __init__(self, nombre: str, tipo: str, direccion: str, codigo_postal: str, 
                 longitud: str, latitud: str, descripcion: str, localidad_codigo: int):
        self.nombre = nombre
        self.tipo = tipo
        self.direccion = direccion
        self.codigo_postal = codigo_postal
        self.longitud = longitud
        self.latitud = latitud
        self.descripcion = descripcion
        self.localidad_codigo = localidad_codigo

    def to_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "tipo": self.tipo,
            "direccion": self.direccion,
            "codigo_postal": self.codigo_postal,
            "longitud": self.longitud,
            "latitud": self.latitud,
            "descripcion": self.descripcion,
            "localidad_codigo": self.localidad_codigo
        }

def get_monumento_filters(nombre: Optional[str] = None, tipo: Optional[str] = None, 
                          localidad_codigo: Optional[int] = None) -> List[str]:
    filters = []
    if nombre:
        filters.append(f"nombre ILIKE '%{nombre}%'")
    if tipo:
        filters.append(f"tipo ILIKE '%{tipo}%'")
    if localidad_codigo is not None:
        filters.append(f"localidad_codigo = {localidad_codigo}")
    return filters