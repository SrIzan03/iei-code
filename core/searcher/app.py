from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from main import router

DATABASE_URL = "postgresql://root:root@localhost:5432/postgres"  # Cambia esto a tu URL de base de datos

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

app.include_router(router)

class Item(Base):
    __tablename__ = "monumentos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    tipo = Column(String, index=True)
    direccion = Column(String, index=True)
    localidad = Column(String, index=True)
    codigoPostal = Column(String, index=True)
    provincia = Column(String, index=True)
    descripcion = Column(String, index=True)

Base.metadata.create_all(bind=engine)

class ItemResponse(BaseModel):
    nombre: str
    tipo: str
    direccion: str
    localidad: str
    codigoPostal: str
    provincia: str
    descripcion: str

@app.get("/search/", response_model=list[ItemResponse])
async def search_items(
    localidad: int = Query(None, min_length=3, max_length=50),
    codigoPostal: str = Query(None, min_length=3, max_length=50),
    provincia: str = Query(None, min_length=3, max_length=50),
    tipo: str = Query(None, min_length=3, max_length=50)
):
    session = SessionLocal()
    try:
        query = session.query(Item)
        
        if localidad:
            query = query.filter(Item.id == id)
        
        if codigoPostal:
            query = query.filter(Item.name.contains(codigoPostal))
        
        if provincia:
            query = query.filter(Item.description.contains(provincia))
        
        if tipo:
            query = query.filter(Item.tipo == tipo)
        
        results = query.all()
        
        if not results:
            raise HTTPException(status_code=404, detail="No items found")
        
        return results
    
    finally:
        session.close()
