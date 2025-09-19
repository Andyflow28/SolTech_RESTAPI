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
    station_id: str = Field(..., pattern="^[0-9a-fA-F]+$", description="Station ID must be a valid hexadecimal string")  # Cambiado a str

class UserStation(UserStationBase):
    station_id: str  # Cambiado a str
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)

# StationData schemas
class StationDataBase(BaseModel):
    # Datos del sensor AHT20
    temperature_aht20: Optional[float] = Field(None, ge=-40, le=80, description="Temperature from AHT20 must be between -40 and 80°C")
    humidity_aht20: Optional[float] = Field(None, ge=0, le=100, description="Humidity from AHT20 must be between 0 and 100%")
    
    # Datos del sensor BMP280
    temperature_bmp280: Optional[float] = Field(None, ge=-40, le=80, description="Temperature from BMP280 must be between -40 and 80°C")
    pressure_bmp280: Optional[float] = Field(None, ge=300, le=1100, description="Pressure from BMP280 in hPa")
    
    # Datos del sensor MQ-2
    voltage_mq2: Optional[float] = Field(None, ge=0, le=5, description="Voltage from MQ-2 between 0 and 5V")
    digital_mq2: Optional[bool] = Field(None, description="Digital output from MQ-2: True if gas detected")
    
    # Datos del sensor MQ-135
    voltage_mq135: Optional[float] = Field(None, ge=0, le=5, description="Voltage from MQ-135 between 0 and 5V")
    digital_mq135: Optional[bool] = Field(None, description="Digital output from MQ-135: True if gas detected")

class StationDataCreate(StationDataBase):
    station_id: str = Field(..., pattern="^[0-9a-fA-F]+$", description="Station ID must be a valid hexadecimal string")  # Cambiado a str

class StationData(StationDataBase):
    id: int
    station_id: str  # Cambiado a str
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    device_id: Optional[str] = None