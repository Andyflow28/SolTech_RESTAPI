from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base


class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    has_station = Column(Boolean, default=False, nullable=False)

    stations = relationship("UserStation", back_populates="user")


class UserStation(Base):
    __tablename__ = "user_stations"
    
    station_id = Column(String, primary_key=True, index=True)
    location = Column(String, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    user = relationship("User", back_populates="stations")
    
    station_data = relationship("StationData", back_populates="station")


class StationData(Base):
    __tablename__ = "station_data"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos de ambiente (combinación de AHT20 y BMP280)
    temperatura = Column(Float, nullable=True) # Sustituye a temperature_aht20/bmp280
    humedad = Column(Float, nullable=True)     # Sustituye a humidity_aht20
    presion = Column(Float, nullable=True)     # Sustituye a pressure_bmp280
    
    # Datos del sensor MQ-135 (Simplificado y renombrado)
    gas_detectado = Column(Boolean, nullable=True)  # Sustituye a digital_mq135
    voltaje_mq135 = Column(Float, nullable=True)  # Mantenido/Renombrado
    
    # Datos del UV
    indice_uv = Column(Float, nullable=True)
    nivel_uv = Column(String, nullable=True)   # Nuevo campo de texto

    # Foreign key con UserStation
    station_id = Column(String, ForeignKey("user_stations.station_id"), nullable=False)
    station = relationship("UserStation", back_populates="station_data")
    
    # Timestamp
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)