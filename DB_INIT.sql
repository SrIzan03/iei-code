-- Crear la tabla Provincia
CREATE TABLE Provincia (
    codigo INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);

-- Crear la tabla Localidad
CREATE TABLE Localidad (
    codigo INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    provincia_codigo INTEGER NOT NULL,
    FOREIGN KEY (provincia_codigo) REFERENCES Provincia(codigo)
);

-- Crear la tabla Monumento
CREATE TABLE Monumento (
    nombre TEXT PRIMARY KEY,
    tipo TEXT NOT NULL CHECK (tipo IN ('Yacimiento arqueológico', 'Iglesia-Ermita', 
                                       'Monasterio-Convento', 'Castillo-Fortaleza-Torre', 
                                       'Edificio singular', 'Puente', 'Otros')),
    direccion TEXT,
    codigo_postal TEXT,
    longitud REAL,
    latitud REAL,
    descripcion TEXT,
    localidad_codigo INTEGER NOT NULL,
    FOREIGN KEY (localidad_codigo) REFERENCES Localidad(codigo)
);