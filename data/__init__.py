from .localidad_repository import (
    create_localidad,
    get_localidad_by_nombre,
    create_localidad
)
from .monumento_repository import (
    create_monumento,
    get_monumento_by_nombre,
    create_monumento
)
from .provincia_repository import (
    create_provincia,
    get_provincia_by_nombre,
    create_provincia
)

__all__ = [
    'create_localidad',
    'get_localidad_by_nombre',
    'create_monumento',
    'get_monumento_by_nombre',
    'create_provincia',
    'get_provincia_by_nombre'
]