from sqlalchemy.orm import Session
from . import models, schemas
from .security import hash_password
from datetime import datetime, timezone, timedelta
from typing import List, Optional

# User CRUD operations
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password) 
    
    db_user = models.User(
        email=user.email,
        username=user.username,
        password=hashed_password,
        full_name=user.full_name,
        has_station=False
    )
    db.add(db_user) 
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# UserStation CRUD operations
def create_user_station(db: Session, user_station: schemas.UserStationCreate):
    db_user_station = models.UserStation(
        station_id=user_station.station_id,  # Ahora es string
        location=user_station.location,
        user_id=user_station.user_id
    )
    db.add(db_user_station)
    
    # Update the user's has_station flag
    user_with_station = db.query(models.User).filter(models.User.user_id == user_station.user_id).first()
    if user_with_station:
        user_with_station.has_station = True
    
    db.commit()
    db.refresh(db_user_station)
    return db_user_station

def get_user_station(db: Session, station_id: str):  # Cambiado a str
    return db.query(models.UserStation).filter(models.UserStation.station_id == station_id).first()

def get_user_stations_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.UserStation).filter(
        models.UserStation.user_id == user_id
    ).offset(skip).limit(limit).all()

def get_all_user_stations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserStation).offset(skip).limit(limit).all()

# StationData CRUD operations (updated for new sensors)
def create_station_data(db: Session, data: schemas.StationDataCreate):
    db_obj = models.StationData(
        temperature_aht20=data.temperature_aht20,
        humidity_aht20=data.humidity_aht20,
        temperature_bmp280=data.temperature_bmp280,
        pressure_bmp280=data.pressure_bmp280,
        voltage_mq2=data.voltage_mq2,
        digital_mq2=data.digital_mq2,
        voltage_mq135=data.voltage_mq135,
        digital_mq135=data.digital_mq135,
        station_id=data.station_id,  # Ahora es string
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_station_data(db: Session, skip: int = 0, limit: int = 100, 
                   station_id: str = None, start_time: datetime = None,  # Cambiado a str
                   end_time: datetime = None):
    query = db.query(models.StationData)
    
    if station_id:
        query = query.filter(models.StationData.station_id == station_id)
    
    if start_time:
        query = query.filter(models.StationData.timestamp >= start_time)
    
    if end_time:
        query = query.filter(models.StationData.timestamp <= end_time)
    
    return query.order_by(models.StationData.timestamp.desc()).offset(skip).limit(limit).all()

def get_station_data_by_id(db: Session, data_id: int):
    return db.query(models.StationData).filter(models.StationData.id == data_id).first()

def get_latest_station_data(db: Session, station_id: str = None, limit: int = 10):  # Cambiado a str
    query = db.query(models.StationData)
    
    if station_id:
        query = query.filter(models.StationData.station_id == station_id)
    
    return query.order_by(models.StationData.timestamp.desc()).limit(limit).all()

def delete_old_station_data(db: Session, days: int = 30):
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days) 
    result = db.query(models.StationData).filter(models.StationData.timestamp < cutoff_date).delete()
    db.commit()
    return result