-- Crear la tabla Provincia
CREATE TABLE Provincia (
    codigo SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

-- Crear la tabla Localidad
CREATE TABLE Localidad (
    codigo SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    provincia_codigo INTEGER NOT NULL,
    FOREIGN KEY (provincia_codigo) REFERENCES Provincia(codigo)
);

-- Crear la tabla Monumento
CREATE TABLE Monumento (
    nombre TEXT PRIMARY KEY,
    tipo TEXT NOT NULL CHECK (tipo IN ('Yacimiento arqueologico', 'Iglesia-Ermita', 
                                       'Monasterio-Convento', 'Castillo-Fortaleza-Torre', 
                                       'Edificio singular', 'Puente', 'Otros')),
    direccion TEXT,
    codigo_postal TEXT,
    longitud DOUBLE PRECISION,
    latitud DOUBLE PRECISION,
    descripcion TEXT,
    localidad_codigo INTEGER NOT NULL,
    FOREIGN KEY (localidad_codigo) REFERENCES Localidad(codigo)
);