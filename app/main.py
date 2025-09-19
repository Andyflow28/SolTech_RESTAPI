from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel

from . import models, schemas, crud
from .database import SessionLocal, engine
from .config import settings
from .security import create_access_token, verify_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ESP32 Sensor API",
    description="API para recibir datos de sensores desde dispositivos ESP32",
    version="1.0.0"
)

# CORS middleware
origins = settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS else []
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Esquema para login de usuarios
class UserLogin(BaseModel):
    email: str
    password: str

## User endpoints
@app.post("/users", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return crud.create_user(db=db, user=user)

@app.get("/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

## Nuevo endpoint para autenticación de usuarios
@app.post("/auth/login")
def user_login(credentials: UserLogin, db: Session = Depends(get_db)):
    # Buscar usuario por email
    user = crud.get_user_by_email(db, email=credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # Verificar contraseña
    if not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # Crear token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": user.user_id,
        "email": user.email,
        "full_name": user.full_name
    }

## UserStation endpoints
@app.post("/user-stations", response_model=schemas.UserStation, status_code=status.HTTP_201_CREATED)
def create_user_station(
    user_station: schemas.UserStationCreate, 
    db: Session = Depends(get_db)
):
    # Check if user exists
    db_user = crud.get_user(db, user_id=user_station.user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if station_id already exists
    db_station = crud.get_user_station(db, station_id=user_station.station_id)
    if db_station:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Station ID already exists"
        )
    
    return crud.create_user_station(db=db, user_station=user_station)

@app.get("/user-stations", response_model=List[schemas.UserStation])
def read_user_stations(
    skip: int = 0, 
    limit: int = 100, 
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db)
):
    if user_id:
        return crud.get_user_stations_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return crud.get_all_user_stations(db, skip=skip, limit=limit)

@app.get("/user-stations/{station_id}", response_model=schemas.UserStation)
def read_user_station(station_id: str, db: Session = Depends(get_db)):
    db_station = crud.get_user_station(db, station_id=station_id)
    if db_station is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Station not found"
        )
    return db_station

## StationData endpoints
@app.post("/station-data", response_model=schemas.StationData, status_code=status.HTTP_201_CREATED)
def create_station_data(
    payload: schemas.StationDataCreate, 
    db: Session = Depends(get_db)
):
    try:
        db_station = crud.get_user_station(db, station_id=payload.station_id)
        if not db_station:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Station with ID {payload.station_id} not found"
            )
            
        obj = crud.create_station_data(db, payload)
        return obj
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error storing station data: {str(e)}"
        )

@app.get("/station-data", response_model=List[schemas.StationData])
def read_station_data(
    skip: int = 0,
    limit: int = 100,
    station_id: Optional[str] = Query(None, description="Filter by station ID (hexadecimal)"),
    start_time: Optional[datetime] = Query(None, description="Start time filter"),
    end_time: Optional[datetime] = Query(None, description="End time filter"),
    db: Session = Depends(get_db)
):
    return crud.get_station_data(db, skip=skip, limit=limit, station_id=station_id, 
                               start_time=start_time, end_time=end_time)

@app.get("/station-data/latest", response_model=List[schemas.StationData])
def read_latest_station_data(
    station_id: Optional[str] = Query(None, description="Specific station ID (hexadecimal)"),
    limit: int = Query(10, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    return crud.get_latest_station_data(db, station_id=station_id, limit=limit)

@app.get("/station-data/{data_id}", response_model=schemas.StationData)
def read_station_data_id(data_id: int, db: Session = Depends(get_db)):
    obj = crud.get_station_data_by_id(db, data_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record with ID {data_id} not found"
        )
    return obj

@app.delete("/station-data/cleanup")
def cleanup_old_station_data(
    days: int = Query(30, ge=1, description="Delete data older than this many days"),
    db: Session = Depends(get_db)
):
    deleted_count = crud.delete_old_station_data(db, days)
    return {"detail": f"Deleted {deleted_count} old records"}

## Authentication endpoints
@app.post("/token")
def create_token(device_id: str):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": device_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

## Health check endpoint
@app.get("/health")
def health_check():
    # Corrected to use a timezone-aware datetime object
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc)}
    
# Render Section
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 