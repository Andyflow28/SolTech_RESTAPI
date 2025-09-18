from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base  # suponiendo que tienes un archivo database.py con la Base declarada


class User(Base):
    __tablename__ = "user"
    
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    has_station = Column(Boolean, default=False, nullable=False)  # Nuevo campo

    # Relación con UserStation
    stations = relationship("UserStation", back_populates="user")


class UserStation(Base):
    __tablename__ = "user_station"
    
    station_id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)  # Nuevo campo que sustituye a Region.location
    
    # Foreign key con User
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    user = relationship("User", back_populates="stations")
    
    # Relación con StationData
    station_data = relationship("StationData", back_populates="station")


class StationData(Base):
    __tablename__ = "station_data"
    
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    
    # Foreign key con UserStation
    station_id = Column(Integer, ForeignKey("user_station.station_id"), nullable=False)
    station = relationship("UserStation", back_populates="station_data")
    
    # Use a timezone-aware datetime for the default timestamp
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
