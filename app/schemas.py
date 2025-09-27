from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class User(UserBase):
    user_id: int
    has_station: bool
    
    model_config = ConfigDict(from_attributes=True)

# UserStation schemas
class UserStationBase(BaseModel):
    location: str = Field(..., max_length=100)

class UserStationCreate(UserStationBase):
    user_id: int
    station_id: str = Field(..., pattern="^[0-9a-fA-F]+$", description="Station ID must be a valid hexadecimal string")

class UserStation(UserStationBase):
    station_id: str
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)

# StationData schemas (NUEVA ESTRUCTURA)
class StationDataBase(BaseModel):
    # Datos de ambiente
    temperatura: Optional[float] = Field(None, ge=-40, le=80, description="Temperatura en °C")
    humedad: Optional[float] = Field(None, ge=0, le=100, description="Humedad en %")
    presion: Optional[float] = Field(None, ge=300, le=1100, description="Presión en hPa")
    
    # Datos de gas
    gas_detectado: Optional[bool] = Field(None, description="True si se detectó gas (MQ-135)")
    voltaje_mq135: Optional[float] = Field(None, ge=0, le=5, description="Voltaje del sensor MQ-135")
    
    # Datos del UV
    indice_uv: Optional[float] = Field(None, ge=0, le=15, description="Valor del índice UV")
    nivel_uv: Optional[str] = Field(None, description="Descripción del nivel UV (e.g., 'Bajo', 'Alto')")

class StationDataCreate(StationDataBase):
    station_id: str = Field(..., pattern="^[0-9a-fA-F]+$", description="Station ID must be a valid hexadecimal string")

class StationData(StationDataBase):
    id: int
    station_id: str
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    device_id: Optional[str] = None