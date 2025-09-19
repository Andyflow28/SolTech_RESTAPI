from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base


class User(Base):
    __tablename__ = "users"  # Cambiado de "user" a "users" (plural)
    
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    has_station = Column(Boolean, default=False, nullable=False)

    # Relación con UserStation
    stations = relationship("UserStation", back_populates="user")


class UserStation(Base):
    __tablename__ = "user_stations"  # Cambiado a plural para consistencia
    
    station_id = Column(String, primary_key=True, index=True)  # Ahora es string
    location = Column(String, nullable=False)
    
    # Foreign key con User (actualizado para referenciar la tabla correcta)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)  # Cambiado a "users.user_id"
    user = relationship("User", back_populates="stations")
    
    # Relación con StationData
    station_data = relationship("StationData", back_populates="station")


class StationData(Base):
    __tablename__ = "station_data"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos del sensor AHT20
    temperature_aht20 = Column(Float, nullable=True)
    humidity_aht20 = Column(Float, nullable=True)
    
    # Datos del sensor BMP280
    temperature_bmp280 = Column(Float, nullable=True)
    pressure_bmp280 = Column(Float, nullable=True)
    
    # Datos del sensor MQ-2
    voltage_mq2 = Column(Float, nullable=True)
    digital_mq2 = Column(Boolean, nullable=True)
    
    # Datos del sensor MQ-135
    voltage_mq135 = Column(Float, nullable=True)
    digital_mq135 = Column(Boolean, nullable=True)
    
    # Foreign key con UserStation (actualizado para referenciar la tabla correcta)
    station_id = Column(String, ForeignKey("user_stations.station_id"), nullable=False)  # Cambiado a "user_stations.station_id"
    station = relationship("UserStation", back_populates="station_data")
    
    # Timestamp
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)