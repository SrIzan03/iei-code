from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://root:root@localhost:5431/postgres"  # Cambia esto a tu URL de base de datos

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class Monumento(Base):
    __tablename__ = "Monumento"
    nombre = Column(String, primary_key=True)
    tipo = Column(String)
    direccion = Column(String)
    codigo_postal = Column(String)
    longitud = Column(String)
    latitud = Column(String)
    descripcion = Column(String)
    localidad_codigo = Column(Integer)

Base.metadata.create_all(bind=engine)

class MonumentoResponse(BaseModel):
    nombre: str
    tipo: str
    direccion: str
    codigo_postal: str
    longitud: float
    latitud: float
    descripcion: str
    localidad_codigo: int

    class Config:
        orm_mode = True

@app.get("/search/", response_model=list[MonumentoResponse])
async def search_items(
    localidad: str = Query(None, min_length=3, max_length=50),
    codigo_postal: str = Query(None, min_length=3, max_length=50),
    provincia: str = Query(None, min_length=3, max_length=50),
    tipo: str = Query(None, min_length=3, max_length=50)
):
    session = SessionLocal()
    try:
        query = session.query(Monumento)
        
        if localidad:
            query = query.filter(Monumento.localidad_codigo.contains(localidad))
        
        if codigo_postal:
            query = query.filter(Monumento.codigo_postal.contains(codigo_postal))
        
        if provincia:
            query = query.filter(Monumento.descripcion.contains(provincia))
        
        if tipo:
            query = query.filter(Monumento.tipo == tipo)
        
        results = query.all()
        
        if not results:
            raise HTTPException(status_code=404, detail="No items found")
        
        return results
    
    finally:
        session.close()
